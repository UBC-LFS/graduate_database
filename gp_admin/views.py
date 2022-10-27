from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
import hashlib

from .models import *
from .forms import *
from . import api

from scheduler import tasks


def index(request):
    # tasks.get_sis_students()
    print( request.session.get('loggedin_user') )

    return render(request, 'gp_admin/index.html')


# Student


class Get_Students(View):
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


class Create_Student(View):
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
                'basic_info': api.build_url(request.path, next, 'basic_info'),
                'additional_info': api.build_url(request.path, next, 'additional_info'),
                'previous_school_info': api.build_url(request.path, next, 'previous_school_info')
            }
        })

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


def cancel_student(request):

    # Delete forms in session if they exist
    if 'basic_info_form' in request.session:
        del request.session['basic_info_form']
    if 'additional_info_form' in request.session:
        del request.session['additional_info_form']
    if 'previous_school_info_form' in request.session:
        del request.session['previous_school_info_form']

    return HttpResponseRedirect(request.GET.get('next'))


class Edit_Student(View):
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
                'basic_info': api.build_url(request.path, next, 'basic_info'),
                'additional_info': api.build_url(request.path, next, 'additional_info'),
                'previous_school_info': api.build_url(request.path, next, 'previous_school_info')
            }
        })

    def post(self, request, *args, **kwargs):
        tab = request.POST.get('tab')
        stud = api.get_student(kwargs.get('student_number'))
        
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


class Get_Professors(View):
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


class Edit_Professor(View):
    prof_form = Professor_Form

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


class Get_Grad_Supervision(View):
    def get(self, request, *args, **kwargs):
        prof_list = api.get_professors()

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
            if prof.profile.roles.filter(slug='graduate-advisor').exists():
                prof.is_grad_advisor = True

        return render(request, 'gp_admin/data_tables/get_grad_supervision.html', {
            'professors': professors,
            'total_professors': len(prof_list)
        })


class Add_Grad_Supervision(View):
    form = Grad_Supervision_Form
    def get(self, request, *args, **kwargs):
        prof = api.get_professor(kwargs.get('username'), 'username')
        return render(request, 'gp_admin/data_tables/add_grad_supervision.html', {
            'prof': prof,
            'form': self.form,
            'prof_roles': Professor_Role.objects.all(),
            'next': request.GET.get('next')
        })

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
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))
        return HttpResponseRedirect( reverse('gp_admin:add_grad_supervision', args=[kwargs.get('username')]) + '?next=' + request.POST.get('next') )


@require_http_methods(['POST'])
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


@require_http_methods(['POST'])
def delete_grad_supervision(request, username):
    gs = api.get_grad_supervision(request.POST.get('graduate_supervision'))
    if gs.delete():
        messages.success(request, 'Success! Graduate Supervision ({0} {1}) deleted.'.format(gs.student.first_name, gs.student.last_name))
    else:
        messages.error(request, 'An error occurred while deleting this graduate supervision.')
    return HttpResponseRedirect( reverse('gp_admin:add_grad_supervision', args=[username]) + '?next=' + request.POST.get('next') )


class Get_Comp_Exams(View):
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

    def post(self, request, *args, **kwargs):
        pass

class Sent_Reminders(View):
    def get(self, request, *args, **kwargs):
        # tasks.send_reminders()
        sent_reminders = api.sent_reminders()

        return render(request, 'gp_admin/data_tables/sent_reminders.html', {
            'reminders': sent_reminders,
            'total_reminders': len(sent_reminders)
        })

    def post(self, request, *args, **kwargs):
        pass


# Users

class Get_Users(View):
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

    def post(self, request, *args, **kwargs):
        pass


class Create_User(View):
    user_form = User_Form
    profile_form = Profile_Form
    prof_form = Professor_Form

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
                'basic_info': api.build_url(request.path, next, 'basic_info'),
                'role_details': api.build_url(request.path, next, 'role_details')
            }
        })

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


def cancel_user(request):

    # Delete a form session if it exists
    if 'save_user_profile_form' in request.session:
        del request.session['save_user_profile_form']
    if 'save_prof_form' in request.session:
        del request.session['save_prof_form']

    return HttpResponseRedirect( request.GET.get('next') )


class Edit_User(View):
    user_form = User_Form
    profile_form = Profile_Form
    prof_form = Professor_Form

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
                'basic_info': api.build_url(request.path, next, 'basic_info'),
                'role_details': api.build_url(request.path, next, 'role_details')
            }
        })

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


"""def save_user(request):
    data = request.GET
    path = request.GET.get('path')
    if path == 'basic_user':
        roles = request.GET.getlist('roles[]', [])
        if len(roles) == 0:
            roles = [ request.GET.get('roles', '') ]

        request.session['save_user_profile_form'] = {
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'email': data.get('email', ''),
            'username': data.get('username', ''),
            'is_superuser': data.get('is_superuser') if data.get('is_superuser', None) else '',
            'is_active': data.get('is_active') if data.get('is_active', None) else '',
            'preferred_name': data.get('preferred_name', ''),
            'roles': roles,
            'phone': data.get('phone', ''),
            'office': data.get('office', '')
        }
    elif path == 'role_details':
        programs = request.GET.getlist('programs[]', [])
        if len(programs) == 0:
            programs = [ request.GET.get('programs', '') ]

        request.session['save_prof_form'] = {
            'title': data.get('title', ''),
            'position': data.get('position', ''),
            'programs': programs,
            
        }

    return JsonResponse({ 'status': 'success', 'message': 'Success! {0} Form saved.'.format(path) })


    user_form = self.user_form(request.POST, instance=user)
    profile_form = self.profile_form(request.POST, instance=user.profile)

    errors = []
    if not user_form.is_valid():
        errors.append( api.get_error_messages(user_form.errors.get_json_data()) )
    if not profile_form.is_valid():
        errors.append( api.get_error_messages(profile_form.errors.get_json_data()) )

    if len(errors) == 0:
        # profile_roles = user.profile.roles.all()
        user_form.save()
        profile = profile_form.save()

        # res = api.update_profile_roles(profile, profile_roles, profile_form.cleaned_data)
        messages.success(request, 'Success! User ({0}, CWL: {1}) updated'.format(user.get_full_name(), user.username))
        return redirect('gp_admin:get_users')
    else:
        messages.error(request, 'An error occurred. Form is invalid. {0}'.format(' '.join(errors)) )

    return redirect('gp_admin:edit_user')"""


"""def post_user(session, post):
    ''' Helper function to add or edit a user '''
    
    # user_id = request.POST.get('user', None)
    # print('user_id', user_id)
    # user = api.get_user(user_id)

    current_tab = post.get('current_tab')

    user_profile_data = post
    prof_data = post

    if current_tab == 'User':
        prof_data = session.get('save_prof_form', None)
    elif current_tab == 'Professor':
        user_profile_data = session.get('save_user_profile_form', None)

    user_form = User_Form(user_profile_data)
    profile_form = Profile_Form(user_profile_data)
    prof_form = Professor_Form(prof_data)

    errors = []
    if user_profile_data:
        if not user_form.is_valid():
            errors.append( api.get_error_messages(user_form.errors.get_json_data()) )
        if not profile_form.is_valid():
            errors.append( api.get_error_messages(profile_form.errors.get_json_data()) )

    if prof_data and not prof_form.is_valid():
        errors.append( api.get_error_messages(prof_form.errors.get_json_data()) )

    if len(errors) == 0:
        user = user_form.save()
        profile = api.create_profile(user)

        # Create a profile and add roles and programs if they exist
        update_fields = []
        if user_profile_data:
            profile_data = profile_form.cleaned_data

            profile.preferred_name = profile_data.get('preferred_name', None)
            profile.phone = profile_data.get('phone', None)
            profile.office = profile_data.get('office', None)

            roles = profile_data.get('roles', None)
            if roles:
                profile.roles.add( *roles )

            update_fields.extend( ['preferred_name', 'phone', 'office'] )

        if prof_data:
            prof_data = prof_form.cleaned_data

            profile.title = prof_data.get('title', None)
            profile.position = prof_data.get('position', None)
            
            programs = prof_data.get('programs', None)
            if programs:
                profile.programs.add( *programs )

            update_fields.extend( ['title', 'position'] )

        profile.save(update_fields=update_fields)

        # Delete a form session if it exists
        if 'save_user_profile_form' in session:
            del session['save_user_profile_form']
        if 'save_prof_form' in session:
            del session['save_prof_form']

        messages.success(request, 'Success! User ({0} {1}, CWL: {2}) created'.format(user.first_name, user.last_name, user.username))
        return HttpResponseRedirect(post.get('next'))
    else:
        messages.error(request, 'An error occurred. Form is invalid. {0}'.format(' '.join(errors)) )

    return HttpResponseRedirect(post.get('current_page'))"""






# Roles


class Get_Roles(View):
    form_class = Role_Form

    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/users/get_roles.html', {
            'roles': Role.objects.all().order_by('id'),
            'form': self.form_class()
        })

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


@require_http_methods(['POST'])
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


@require_http_methods(['POST'])
def delete_role(request):
    ''' Delete a role '''

    role = api.get_role(request.POST.get('role'))
    if role.delete():
        messages.success(request, 'Success! Role ({0}) deleted'.format(role.name))
    else:
        messages.error(request, 'An error occurred.')
    return redirect('gp_admin:get_roles')



# Preparation


class Get_Statuses(View):
    form_class = Status_Form

    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/preparation/get_statuses.html', {
            'statuses': Status.objects.all().order_by('id'),
            'form': self.form_class()
        })

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


@require_http_methods(['POST'])
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


@require_http_methods(['POST'])
def delete_status(request):
    ''' Delete a status '''

    status = api.get_status(request.POST.get('status'))
    if status.delete():
        messages.success(request, 'Success! Status ({0}) deleted'.format(status.name))
    else:
        messages.error(request, 'An error occurred.')
    return redirect('gp_admin:get_statuses')


class Get_Degrees(View):
    form_class = Degree_Form

    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/preparation/get_degrees.html', {
            'degrees': Degree.objects.all().order_by('id'),
            'form': self.form_class()
        })

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


@require_http_methods(['POST'])
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


@require_http_methods(['POST'])
def delete_degree(request):
    ''' Delete a degree '''

    degree = api.get_degree(request.POST.get('degree'))
    if degree.delete():
        messages.success(request, 'Success! Degree ({0}) deleted'.format(degree.name))
    else:
        messages.error(request, 'An error occurred.')

    return redirect('gp_admin:get_degrees')


class Get_Programs(View):
    form_class = Program_Form

    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/preparation/get_programs.html', {
            'programs': Program.objects.all().order_by('id'),
            'form': self.form_class()
        })

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


@require_http_methods(['POST'])
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


@require_http_methods(['POST'])
def delete_program(request):
    ''' Delete a program '''

    program = api.get_program(request.POST.get('program'))
    if program.delete():
        messages.success(request, 'Success! Program ({0}) deleted'.format(program.name))
    else:
        messages.error(request, 'An error occurred.')

    return redirect('gp_admin:get_programs')


class Get_Titles(View):
    form_class = Title_Form

    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/preparation/get_titles.html', {
            'titles': Title.objects.all().order_by('id'),
            'form': self.form_class()
        })

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


@require_http_methods(['POST'])
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


@require_http_methods(['POST'])
def delete_title(request):
    ''' Delete a title '''

    title = api.get_title(request.POST.get('title'))
    if title.delete():
        messages.success(request, 'Success! Title ({0}) deleted'.format(title.name))
    else:
        messages.error(request, 'An error occurred.')

    return redirect('gp_admin:get_titles')


class Get_Positions(View):
    form_class = Position_Form

    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/preparation/get_positions.html', {
            'positions': Position.objects.all().order_by('id'),
            'form': self.form_class()
        })

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


@require_http_methods(['POST'])
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


@require_http_methods(['POST'])
def delete_position(request):
    ''' Delete a position '''

    position = api.get_position(request.POST.get('position'))
    if position.delete():
        messages.success(request, 'Success! Position ({0}) deleted'.format(position.name))
    else:
        messages.error(request, 'An error occurred.')

    return redirect('gp_admin:get_positions')



class Get_Professor_Roles(View):
    form_class = Professor_Role_Form

    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/preparation/get_professor_roles.html', {
            'professor_roles': Professor_Role.objects.all().order_by('id'),
            'form': self.form_class()
        })

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


@require_http_methods(['POST'])
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


@require_http_methods(['POST'])
def delete_professor_role(request):
    ''' Delete a professor role '''

    professor_role = api.get_professor_role(request.POST.get('professor_role'))
    if professor_role.delete():
        messages.success(request, 'Success! Professor Role ({0}) deleted'.format(professor_role.name))
    else:
        messages.error(request, 'An error occurred.')
    return redirect('gp_admin:get_professor_roles')


class Get_Reminders(View):
    reminder_form = Reminder_Form

    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/data_tables/get_reminders.html', {
            'reminders': Reminder.objects.all().order_by('id'),
            'form': self.reminder_form()
        })

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


class Edit_Reminder(View):
    reminder_form = Reminder_Form

    def get(self, request, *args, **kwargs):
        reminder = api.get_reminder(kwargs['slug'], 'slug')
        return render(request, 'gp_admin/data_tables/edit_reminder.html', {
            'form': self.reminder_form(data=None, instance=reminder)
        })

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


@require_http_methods(['POST'])
def delete_reminder(request):
    ''' Delete a reminder '''

    reminder = api.get_reminder(request.POST.get('reminder'))
    if reminder.delete():
        messages.success(request, 'Success! Reminder (Type: {0}) deleted'.format(reminder.type))
    else:
        messages.error(request, 'An error occurred while deleting it.')

    return redirect('gp_admin:get_reminders')
