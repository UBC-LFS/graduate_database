from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control, never_cache
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.db.models import Q
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.urls import resolve
from urllib.parse import urlparse
import json
import hashlib

from .models import *
from .forms import *
from . import api
from core.auth import superadmin_access_only, admin_access_only

from scheduler import tasks


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['GET'])
@admin_access_only
def index(request):
    # tasks.get_sis_students()
    print( request.session.get('loggedin_user') )

    return render(request, 'gp_admin/index.html', {
        'num_students': len(api.get_students()),
        'num_professors': len(api.get_professors()),
        'num_users': len(api.get_users())
    })


# Student

@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Get_Students(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        student_list = api.get_students()

        first_name_q = request.GET.get('first_name')
        last_name_q = request.GET.get('last_name')
        student_number_q = request.GET.get('student_number')
        email_q = request.GET.get('email')

        if bool(first_name_q):
            student_list = student_list.filter(first_name__icontains=first_name_q)
        if bool(last_name_q):
            student_list = student_list.filter(last_name__icontains=last_name_q)
        if bool(student_number_q):
            student_list = student_list.filter(student_number__icontains=student_number_q)
        if bool(email_q):
            student_list = student_list.filter(email__icontains=email_q)

        page = request.GET.get('page', 1)
        paginator = Paginator(student_list, settings.PAGE_SIZE)

        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)

        return render(request, 'gp_admin/data_tables/get_students.html', {
            'students': students,
            'total_students': len(student_list)
        })

@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Create_Student(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        next = request.GET.get('next')
        tab = request.GET.get('t')

        form = None
        if tab == 'basic_info':
            form = Basic_Info_Form(initial=request.session.get('basic_info_form', None))

        elif tab == 'additional_info':
            form = Additional_Info_Form(initial=request.session.get('additional_info_form', None))

        elif tab == 'previous_school_info':
            form = Previous_School_Info_Form(initial=request.session.get('previous_school_info_form', None))
        else:
            raise Http404

        return render(request, 'gp_admin/data_tables/create_student.html', {
            'students': api.get_students(),
            'form': form,
            'info': {
                'btn_label': 'Create',
                'type': 'create',
                'path': 'students'
            },
            'next': next,
            'tab': tab,
            'tab_urls': {
                'basic_info': api.build_next_tab_url(request.path, next, 'basic_info'),
                'additional_info': api.build_next_tab_url(request.path, next, 'additional_info'),
                'previous_school_info': api.build_next_tab_url(request.path, next, 'previous_school_info')
            }
        })


    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        tab = request.POST.get('tab')
        data = api.queryset_to_dict(request.POST.copy())

        if 'save' in request.POST.keys():
            if tab == 'basic_info':
                request.session['basic_info_form'] = data
            elif tab == 'additional_info':
                request.session['additional_info_form'] = data
            elif tab == 'previous_school_info':
                request.session['previous_school_info_form'] = data
            else:
                raise Http404
            
            messages.success(request, 'Success! {0}rmation Form saved.'.format( api.split_capitalize(tab) ))
        
        else:
            basic_info = request.session.get('basic_info_form', None)
            additional_info = request.session.get('additional_info_form', None)
            previous_school_info = request.session.get('previous_school_info_form', None)

            if tab == 'basic_info':
                if additional_info: data.update(additional_info)
                if previous_school_info: data.update(previous_school_info)

            elif tab == 'additional_info':
                if basic_info: data.update(basic_info)
                if previous_school_info: data.update(previous_school_info)

            elif tab == 'previous_school_info':
                if basic_info: data.update(basic_info)
                if additional_info: data.update(additional_info)

            else:
                raise Http404

            form = Student_Form(data)
            if form.is_valid():
                res = form.save()
                if res:

                    # Delete forms in session if they exist
                    if 'basic_info_form' in request.session:
                        del request.session['basic_info_form']
                    if 'additional_info_form' in request.session:
                        del request.session['additional_info_form']
                    if 'previous_school_info_form' in request.session:
                        del request.session['previous_school_info_form']
                        
                    messages.success(request, 'Success! Student ({0}, Student #: {1}) created.'.format(res.get_full_name(), res.student_number))
                    return HttpResponseRedirect(request.POST.get('next'))
                else:
                    messages.error(request, 'An error occurred while creating data.')
            else:
                messages.error(request, 'An error occurred. Form is invalid. {0}'.format(api.get_error_messages(form.errors.get_json_data())))
        
        return HttpResponseRedirect(request.POST.get('current_page'))


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['GET'])
@admin_access_only
def cancel_student(request):

    # Delete forms in session if they exist
    if 'basic_info_form' in request.session:
        del request.session['basic_info_form']
    if 'additional_info_form' in request.session:
        del request.session['additional_info_form']
    if 'previous_school_info_form' in request.session:
        del request.session['previous_school_info_form']

    return HttpResponseRedirect(request.GET.get('next'))


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Edit_Student(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        next = request.GET.get('next')
        tab = request.GET.get('t')

        stud = api.get_student(kwargs.get('student_number'))

        form = None
        if tab == 'basic_info':
            form = Basic_Info_Form(instance=stud)

        elif tab == 'additional_info':
            form = Additional_Info_Form(instance=stud)

        elif tab == 'previous_school_info':
            form = Previous_School_Info_Form(instance=stud)

        else:
            raise Http404

        return render(request, 'gp_admin/data_tables/create_student.html', {
            'stud': stud,
            'form': form,
            'info': {
                'btn_label': 'Update',
                'type': 'edit',
                'path': 'students'
            },
            'next': next,
            'tab': tab,
            'tab_urls': {
                'basic_info': api.build_next_tab_url(request.path, next, 'basic_info'),
                'additional_info': api.build_next_tab_url(request.path, next, 'additional_info'),
                'previous_school_info': api.build_next_tab_url(request.path, next, 'previous_school_info')
            }
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        tab = request.POST.get('tab')
        stud = api.get_student(request.POST.get('student'))
        
        form = None
        if tab == 'basic_info':
            form = Basic_Info_Form(request.POST, instance=stud)

        elif tab == 'additional_info':
            form = Additional_Info_Form(request.POST, instance=stud)

        elif tab == 'previous_school_info':
            form = Previous_School_Info_Form(request.POST, instance=stud)

        else:
            raise Http404

        if form.is_valid():
            res = form.save()
            if res:
                messages.success(request, 'Success! Student ({0}, Student #: {1}) updated.'.format(stud.get_full_name(), stud.student_number))
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                messages.error(request, 'An error occurred while updating data.')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(api.get_error_messages(form.errors.get_json_data())))
    
        return HttpResponseRedirect(request.POST.get('current_page'))


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Get_Professors(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        prof_list =  api.get_professors()

        first_name_q = request.GET.get('first_name')
        last_name_q = request.GET.get('last_name')
        cwl_q = request.GET.get('cwl')
        email_q = request.GET.get('email')

        if bool(first_name_q):
            prof_list = prof_list.filter(first_name__icontains=first_name_q)
        if bool(last_name_q):
            prof_list = prof_list.filter(last_name__icontains=last_name_q)
        if bool(cwl_q):
            prof_list = prof_list.filter(username__icontains=cwl_q)
        if bool(email_q):
            prof_list = prof_list.filter(email__icontains=email_q)

        page = request.GET.get('page', 1)
        paginator = Paginator(prof_list, settings.PAGE_SIZE)

        try:
            professors = paginator.page(page)
        except PageNotAnInteger:
            professors = paginator.page(1)
        except EmptyPage:
            professors = paginator.page(paginator.num_pages)

        return render(request, 'gp_admin/data_tables/get_professors.html', {
            'professors': professors,
            'total_professors': len(prof_list)
        })


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Edit_Professor(View):
    prof_form = Professor_Form


    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        prof = api.get_professor(kwargs.get('username'), 'username')
        return render(request, 'gp_admin/data_tables/edit_professor.html', {
            'prof': prof,
            'form': self.prof_form(data=None, instance=prof.profile),
            'info': {
                'btn_label': 'Update',
                'type': 'edit',
                'path': 'professors'
            },
            'next': request.GET.get('next')
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        prof = api.get_professor(kwargs.get('username'), 'username')
        form = self.prof_form(request.POST, instance=prof.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success! Professor ({0}, CWL: {1}) updated'.format(prof.get_full_name(), prof.username))
            return HttpResponseRedirect(request.POST.get('next'))
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors) )
        return HttpResponseRedirect( reverse('gp_admin:edit_student') + '?next=' + request.POST.get('next') )


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Get_Grad_Supervision(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        prof_list = api.get_professors()

        tab = request.GET.get('t')

        first_name_q = request.GET.get('first_name')
        last_name_q = request.GET.get('last_name')

        if bool(first_name_q):
            prof_list = prof_list.filter(first_name__icontains=first_name_q)
        if bool(last_name_q):
            prof_list = prof_list.filter(last_name__icontains=last_name_q)

        page = request.GET.get('page', 1)
        paginator = Paginator(prof_list, 1)

        try:
            professors = paginator.page(page)
        except PageNotAnInteger:
            professors = paginator.page(1)
        except EmptyPage:
            professors = paginator.page(paginator.num_pages)

        for prof in professors:
            prof.is_grad_advisor = False
            prof.colleages = None
            if prof.profile.roles.filter(slug='graduate-advisor').exists():
                prof.is_grad_advisor = True
                programs = [program for program in prof.profile.programs.all()]
                prof.colleages = User.objects.filter( Q(profile__programs__in=programs) & Q(profile__roles__in=[api.get_role('graduate-advisor', 'slug'), api.get_role('supervisor', 'slug')]) ).exclude(id=prof.id).order_by('last_name', 'first_name')

        tab_url = request.path + '?page=' + page
        if bool(first_name_q):
            tab_url += '&first_name=' + first_name_q
        if bool(last_name_q):
            tab_url += '&last_name=' + last_name_q

        return render(request, 'gp_admin/data_tables/get_grad_supervision.html', {
            'professors': professors,
            'total_professors': len(prof_list),
            'tab': tab,
            'tab_urls': {
                'students': tab_url + '&t=students',
                'professors': tab_url + '&t=professors'
            }
        })


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Add_Grad_Supervision(View):
    form = Grad_Supervision_Form

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        
        parse_result = urlparse(request.get_full_path())
        if 'next=' not in parse_result.query:
            raise Http404
        
        return render(request, 'gp_admin/data_tables/add_grad_supervision.html', {
            'prof': api.get_professor(kwargs.get('username'), 'username'),
            'form': self.form,
            'prof_roles': Professor_Role.objects.all(),
            'next': parse_result.query.split('next=')[1]
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        prof = api.get_professor(kwargs.get('username'), 'username')
        
        form = self.form(request.POST)
        if form.is_valid():
            res = form.save()
            if res:
                messages.success(request, 'Success! Graduate Supervision ({0} {1}) added.'.format(res.student.first_name, res.student.last_name))
            else:
                messages.error(request, 'An error occurred while saving data.')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format( api.get_error_messages(form.errors.get_json_data()) ))
        return HttpResponseRedirect( reverse('gp_admin:add_grad_supervision', args=[kwargs.get('username')]) + '?next=' + request.POST.get('next') )


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['GET'])
@admin_access_only
def search_students(request):
    ''' Search students '''
    name = request.GET.get('name')
    
    if bool(name):
        studs = api.get_students_by_name(name)
        print(studs)
        data = []
        for stud in studs:
            data.append({
                'id': stud.id,
                'first_name': stud.first_name,
                'last_name': stud.last_name,
                'student_number': stud.student_number
            })
        return JsonResponse({ 'data': data, 'status': 'success' }, safe=False)
    return JsonResponse({ 'data': [], 'status': 'error' }, safe=False)



@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def edit_grad_supervision(request, username):
    gs = api.get_grad_supervision(request.POST.get('graduate_supervision'))
    form = Grad_Supervision_Form(request.POST, instance=gs)
    if form.is_valid():
        res = form.save()
        if res:
            messages.success(request, 'Success! Graduate Supervision ({0} {1}) updated.'.format(res.student.first_name, res.student.last_name))
        else:
            messages.error(request, 'An error occurred while updating data.')
    else:
        messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))
    return HttpResponseRedirect( reverse('gp_admin:add_grad_supervision', args=[username]) + '?next=' + request.POST.get('next') )


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def delete_grad_supervision(request, username):
    gs = api.get_grad_supervision(request.POST.get('graduate_supervision'))
    if gs.delete():
        messages.success(request, 'Success! Graduate Supervision ({0} {1}) deleted.'.format(gs.student.first_name, gs.student.last_name))
    else:
        messages.error(request, 'An error occurred while deleting this graduate supervision.')
    return HttpResponseRedirect( reverse('gp_admin:add_grad_supervision', args=[username]) + '?next=' + request.POST.get('next') )


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Get_Comp_Exams(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        today = datetime.today().date()
        students = api.get_students()
        reminders = api.get_reminders()
        for stud in students:
            expect_send_reminders = []
            for rem in reminders:
                if stud.start_date:
                    expect_send_reminders.append(stud.start_date + relativedelta(months=rem.months))
                    expect_send_reminders.reverse()
            stud.expect_send_reminders = expect_send_reminders

        return render(request, 'gp_admin/data_tables/get_comp_exams.html', {
            'students': students,
            'total_students': len(students)
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        pass


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Sent_Reminders(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        # tasks.send_reminders()
        sent_reminders = api.sent_reminders()

        return render(request, 'gp_admin/data_tables/sent_reminders.html', {
            'reminders': sent_reminders,
            'total_reminders': len(sent_reminders)
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        pass


# Users


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Get_Users(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        user_list = api.get_users()
        users = api.get_filtered_items(request, user_list, 'users')

        # Delete a form session if it exists
        # TODO
        # if 'user_profile_form' in request.session:
        #     del request.session['user_profile_form']
        # if 'prof_form' in request.session:
        #     del request.session['prof_form']

        return render(request, 'gp_admin/users/get_users.html', {
            'users': users,
            'total_users': len(user_list)
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        pass


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Create_User(View):
    user_form = User_Form
    profile_form = Profile_Form
    prof_form = Professor_Form

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        next = request.GET.get('next')
        tab = request.GET.get('t')
        
        if tab not in ['basic_info', 'role_details']:
            raise Http404

        return render(request, 'gp_admin/users/create_user.html', {
            'users': api.get_users(),
            'user_form': self.user_form(initial=request.session.get('user_profile_form', None)),
            'profile_form': self.profile_form(initial=request.session.get('user_profile_form', None)),
            'prof_form': self.prof_form(initial=request.session.get('prof_form', None)),
            'info': {
                'btn_label': 'Create',
                'href': reverse('gp_admin:create_user'),
                'type': 'create',
                'path': 'users'
            },
            'next': next,
            'tab': tab,
            'tab_urls': {
                'basic_info': api.build_next_tab_url(request.path, next, 'basic_info'),
                'role_details': api.build_next_tab_url(request.path, next, 'role_details')
            }
        })


    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        tab = request.POST.get('tab')
        
        if 'save' in request.POST:

            name = ''
            if tab == 'basic_info':
                request.session['user_profile_form'] = api.queryset_to_dict(request.POST.copy())
                name = api.split_capitalize(tab) + 'rmation'
            elif tab == 'role_details':
                request.session['role_details_form'] = api.queryset_to_dict(request.POST.copy())
                name = api.split_capitalize(tab)
            else:
                raise Http404
            
            messages.success(request, 'Success! {0} Form saved.'.format(name))

        else:
            user_profile_session = request.session.get('user_profile_form', None)
            role_details_session = request.session.get('role_details_form', None)
            
            user_form = None
            profile_form = None
            prof_form = None

            if tab == 'basic_info':
                user_form = self.user_form(request.POST)
                profile_form = self.profile_form(request.POST)
            
                if role_details_session: 
                    prof_form = self.prof_form(role_details_session)

            elif tab == 'role_details':
                prof_form = self.prof_form(request.POST)
            
                if user_profile_session: 
                    user_form = self.user_form(user_profile_session)
                    profile_form = self.profile_form(user_profile_session)
            
            else:
                raise Http404

            errors = []
            if user_form and not user_form.is_valid():
                errors.append( api.get_error_messages(user_form.errors.get_json_data()) )

            if profile_form and not profile_form.is_valid():
                errors.append( api.get_error_messages(profile_form.errors.get_json_data()) )

            if prof_form and not prof_form.is_valid():
                errors.append( api.get_error_messages(prof_form.errors.get_json_data()) )

            if len(errors) == 0:
                user = user_form.save()
                profile = api.create_profile(user)

                # Create a profile and add roles and programs if they exist
                update_fields = []
                if profile_form:
                    profile_data = profile_form.cleaned_data

                    profile.preferred_name = profile_data.get('preferred_name', None)
                    profile.phone = profile_data.get('phone', None)
                    profile.office = profile_data.get('office', None)

                    roles = profile_data.get('roles', None)
                    if roles:
                        profile.roles.add( *roles )

                    update_fields.extend( ['preferred_name', 'phone', 'office'] )

                if prof_form:
                    prof_data = prof_form.cleaned_data

                    profile.title = prof_data.get('title', None)
                    profile.position = prof_data.get('position', None)

                    programs = prof_data.get('programs', None)
                    if programs:
                        profile.programs.add( *programs )

                    update_fields.extend( ['title', 'position'] )

                profile.save(update_fields=update_fields)

                # Delete a form session if it exists
                if 'user_profile_form' in request.session:
                    del request.session['user_profile_form']
                if 'role_details_form' in request.session:
                    del request.session['role_details_form']

                messages.success(request, 'Success! User ({0} {1}, CWL: {2}) created.'.format(user.first_name, user.last_name, user.username))
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                messages.error(request, 'An error occurred. Form is invalid. {0}'.format(' '.join(errors)) )

        return HttpResponseRedirect(request.POST.get('current_page'))


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['GET'])
@admin_access_only
def cancel_user(request):

    # Delete a form session if it exists
    if 'save_user_profile_form' in request.session:
        del request.session['save_user_profile_form']
    if 'save_prof_form' in request.session:
        del request.session['save_prof_form']

    return HttpResponseRedirect( request.GET.get('next') )


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Edit_User(View):
    user_form = User_Form
    profile_form = Profile_Form
    prof_form = Professor_Form

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        next = request.GET.get('next')
        tab = request.GET.get('t')

        user = api.get_user(kwargs.get('username'), 'username')
        profile = api.has_profile_created(user)

        return render(request, 'gp_admin/users/create_user.html', {
            'user': user,
            'user_form': self.user_form(instance=user),
            'profile_form': self.profile_form(instance=profile),
            'prof_form': self.prof_form(instance=profile),
            'info': {
                'btn_label': 'Update',
                'href': reverse('gp_admin:edit_user', args=[ kwargs['username'] ]),
                'type': 'edit',
                'path': None
            },
            'next': next,
            'tab': tab,
            'tab_urls': {
                'basic_info': api.build_next_tab_url(request.path, next, 'basic_info'),
                'role_details': api.build_next_tab_url(request.path, next, 'role_details')
            }
        })


    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        tab = request.POST.get('tab')
        user = api.get_user(request.POST.get('user'))

        user_form = None
        profile_form = None
        prof_form = None

        if tab == 'basic_info':
            user_form = self.user_form(request.POST, instance=user)
            profile_form = self.profile_form(request.POST, instance=user.profile)

        elif tab == 'role_details':
            prof_form = self.prof_form(request.POST, instance=user.profile)
        
        else:
            raise Http404

        errors = []
        
        if user_form and not user_form.is_valid():
            errors.append( api.get_error_messages(user_form.errors.get_json_data()) )

        if profile_form and not profile_form.is_valid():
            errors.append( api.get_error_messages(profile_form.errors.get_json_data()) )

        if prof_form and not prof_form.is_valid():
            errors.append( api.get_error_messages(prof_form.errors.get_json_data()) )

        if len(errors) == 0:
            if user_form: 
                user = user_form.save()

            if profile_form:
                profile_form.save()
            
            if prof_form:
                prof_form.save()

            messages.success(request, 'Success! User ({0} {1}, CWL: {2}) updated.'.format(user.first_name, user.last_name, user.username))
            return HttpResponseRedirect(request.POST.get('next'))
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(' '.join(errors)) )

        return HttpResponseRedirect(request.POST.get('current_page'))



# Roles


@method_decorator([never_cache, login_required, superadmin_access_only], name='dispatch')
class Get_Roles(View):
    form_class = Role_Form

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/users/get_roles.html', {
            'roles': Role.objects.all().order_by('id'),
            'form': self.form_class()
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            res = form.save()
            if res:
                messages.success(request, 'Success! Role ({0}) created'.format(res.name))
            else:
                messages.error(request, 'An error occurred while saving data.')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))
        return redirect('gp_admin:get_roles')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@superadmin_access_only
def edit_role(request, slug):
    ''' Edit a role '''

    role = api.get_role(slug, 'slug')
    form = Role_Form(request.POST, instance=role)
    if form.is_valid():
        res = form.save()
        if res:
            messages.success(request, 'Success! Status ({0}) updated'.format(res.name))
        else:
            messages.error(request, 'An error occurred.')
    else:
        messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))
    return redirect('gp_admin:get_roles')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@superadmin_access_only
def delete_role(request):
    ''' Delete a role '''

    role = api.get_role(request.POST.get('role'))
    if role.delete():
        messages.success(request, 'Success! Role ({0}) deleted'.format(role.name))
    else:
        messages.error(request, 'An error occurred.')
    return redirect('gp_admin:get_roles')



# Preparation


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Get_Statuses(View):
    form_class = Status_Form

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/preparation/get_statuses.html', {
            'statuses': Status.objects.all().order_by('id'),
            'form': self.form_class()
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            res = form.save()
            if res:
                messages.success(request, 'Success! Status ({0}) created'.format(res.name))
            else:
                messages.error(request, 'An error occurred while saving data.')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))
        return redirect('gp_admin:get_statuses')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def edit_status(request, slug):
    ''' Edit a status '''

    status = api.get_status(slug, 'slug')
    form = Status_Form(request.POST, instance=status)
    if form.is_valid():
        res = form.save()
        if res:
            messages.success(request, 'Success! Status ({0}) updated'.format(res.name))
        else:
            messages.error(request, 'An error occurred.')
    else:
        messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))
    return redirect('gp_admin:get_statuses')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def delete_status(request):
    ''' Delete a status '''

    status = api.get_status(request.POST.get('status'))
    if status.delete():
        messages.success(request, 'Success! Status ({0}) deleted'.format(status.name))
    else:
        messages.error(request, 'An error occurred.')
    return redirect('gp_admin:get_statuses')


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Get_Degrees(View):
    form_class = Degree_Form

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/preparation/get_degrees.html', {
            'degrees': Degree.objects.all().order_by('id'),
            'form': self.form_class()
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            res = form.save()
            if res:
                messages.success(request, 'Success! Degree ({0}) created'.format(res.name))
            else:
                messages.error(request, 'An error occurred while saving data.')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))

        return redirect('gp_admin:get_degrees')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def edit_degree(request, slug):
    ''' Edit a degree '''

    degree = api.get_degree(slug, 'slug')
    form = Degree_Form(request.POST, instance=degree)
    if form.is_valid():
        res = form.save()
        if res:
            messages.success(request, 'Success! Degree ({0}) updated'.format(res.name))
        else:
            messages.error(request, 'An error occurred.')
    else:
        messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))

    return redirect('gp_admin:get_degrees')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def delete_degree(request):
    ''' Delete a degree '''

    degree = api.get_degree(request.POST.get('degree'))
    if degree.delete():
        messages.success(request, 'Success! Degree ({0}) deleted'.format(degree.name))
    else:
        messages.error(request, 'An error occurred.')

    return redirect('gp_admin:get_degrees')


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Get_Programs(View):
    form_class = Program_Form

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/preparation/get_programs.html', {
            'programs': Program.objects.all().order_by('id'),
            'form': self.form_class()
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            res = form.save()
            if res:
                messages.success(request, 'Success! Program ({0}) created'.format(res.name))
            else:
                messages.error(request, 'An error occurred while saving data.')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))

        return redirect('gp_admin:get_programs')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def edit_program(request, slug):
    ''' Edit a program '''

    program = api.get_program(slug, 'slug')
    form = Program_Form(request.POST, instance=program)
    if form.is_valid():
        res = form.save()
        if res:
            messages.success(request, 'Success! Program ({0}) updated'.format(res.name))
        else:
            messages.error(request, 'An error occurred.')
    else:
        messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))

    return redirect('gp_admin:get_programs')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def delete_program(request):
    ''' Delete a program '''

    program = api.get_program(request.POST.get('program'))
    if program.delete():
        messages.success(request, 'Success! Program ({0}) deleted'.format(program.name))
    else:
        messages.error(request, 'An error occurred.')

    return redirect('gp_admin:get_programs')


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Get_Titles(View):
    form_class = Title_Form

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/preparation/get_titles.html', {
            'titles': Title.objects.all().order_by('id'),
            'form': self.form_class()
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            res = form.save()
            if res:
                messages.success(request, 'Success! Title ({0}) created'.format(res.name))
            else:
                messages.error(request, 'An error occurred while saving data.')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))
        return redirect('gp_admin:get_titles')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def edit_title(request, slug):
    ''' Edit a title '''

    title = api.get_title(slug, 'slug')
    form = Title_Form(request.POST, instance=title)
    if form.is_valid():
        res = form.save()
        if res:
            messages.success(request, 'Success! Title ({0}) updated'.format(res.name))
        else:
            messages.error(request, 'An error occurred.')
    else:
        messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))

    return redirect('gp_admin:get_titles')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def delete_title(request):
    ''' Delete a title '''

    title = api.get_title(request.POST.get('title'))
    if title.delete():
        messages.success(request, 'Success! Title ({0}) deleted'.format(title.name))
    else:
        messages.error(request, 'An error occurred.')

    return redirect('gp_admin:get_titles')


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Get_Positions(View):
    form_class = Position_Form

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/preparation/get_positions.html', {
            'positions': Position.objects.all().order_by('id'),
            'form': self.form_class()
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            res = form.save()
            if res:
                messages.success(request, 'Success! Position ({0}) created'.format(res.name))
            else:
                messages.error(request, 'An error occurred while saving data.')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))
        return redirect('gp_admin:get_positions')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def edit_position(request, slug):
    ''' Edit a position '''

    position = api.get_position(slug, 'slug')
    form = Position_Form(request.POST, instance=position)
    if form.is_valid():
        res = form.save()
        if res:
            messages.success(request, 'Success! Position ({0}) updated'.format(res.name))
        else:
            messages.error(request, 'An error occurred.')
    else:
        messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))

    return redirect('gp_admin:get_positions')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def delete_position(request):
    ''' Delete a position '''

    position = api.get_position(request.POST.get('position'))
    if position.delete():
        messages.success(request, 'Success! Position ({0}) deleted'.format(position.name))
    else:
        messages.error(request, 'An error occurred.')

    return redirect('gp_admin:get_positions')


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Get_Professor_Roles(View):
    form_class = Professor_Role_Form

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/preparation/get_professor_roles.html', {
            'professor_roles': Professor_Role.objects.all().order_by('id'),
            'form': self.form_class()
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            res = form.save()
            if res:
                messages.success(request, 'Success! Professor Role ({0}) created'.format(res.name))
            else:
                messages.error(request, 'An error occurred while saving data.')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))
        return redirect('gp_admin:get_professor_roles')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def edit_professor_role(request, slug):
    ''' Edit a professor role '''

    professor_role = api.get_professor_role(slug, 'slug')
    form = Professor_Role_Form(request.POST, instance=professor_role)
    if form.is_valid():
        res = form.save()
        if res:
            messages.success(request, 'Success! Position ({0}) updated'.format(res.name))
        else:
            messages.error(request, 'An error occurred.')
    else:
        messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))
    return redirect('gp_admin:get_professor_roles')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def delete_professor_role(request):
    ''' Delete a professor role '''

    professor_role = api.get_professor_role(request.POST.get('professor_role'))
    if professor_role.delete():
        messages.success(request, 'Success! Professor Role ({0}) deleted'.format(professor_role.name))
    else:
        messages.error(request, 'An error occurred.')
    return redirect('gp_admin:get_professor_roles')


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Get_Reminders(View):
    reminder_form = Reminder_Form

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/data_tables/get_reminders.html', {
            'reminders': Reminder.objects.all().order_by('id'),
            'form': self.reminder_form()
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        form = self.reminder_form(request.POST)
        if form.is_valid():
            res = form.save()
            if res:
                messages.success(request, 'Success! Reminder (Type: {0} and Months: {1}) created.'.format(res.type, res.months))
            else:
                messages.error(request, 'An error occurred while saving data.')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))
        return redirect('gp_admin:get_reminders')


@method_decorator([never_cache, login_required, admin_access_only], name='dispatch')
class Edit_Reminder(View):
    reminder_form = Reminder_Form

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        reminder = api.get_reminder(kwargs['slug'], 'slug')
        return render(request, 'gp_admin/data_tables/edit_reminder.html', {
            'form': self.reminder_form(data=None, instance=reminder)
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        reminder = api.get_reminder(kwargs['slug'], 'slug')
        form = self.reminder_form(request.POST, instance=reminder)
        if form.is_valid():
            res = form.save()
            if res:
                messages.success(request, 'Success! Reminder (Type: {0} and Months: {1}) updated.'.format(res.type, res.months))
            else:
                messages.error(request, 'An error occurred while updating data.')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))
        return redirect('gp_admin:get_reminders')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['POST'])
@admin_access_only
def delete_reminder(request):
    ''' Delete a reminder '''

    reminder = api.get_reminder(request.POST.get('reminder'))
    if reminder.delete():
        messages.success(request, 'Success! Reminder (Type: {0}) deleted'.format(reminder.type))
    else:
        messages.error(request, 'An error occurred while deleting it.')

    return redirect('gp_admin:get_reminders')
