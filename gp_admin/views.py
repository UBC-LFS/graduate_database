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

from .models import *
from .forms import *
from . import api

from scheduler import tasks


def index(request):
    # tasks.get_sis_students()
    print( request.session.get('loggedin_user') )

    return render(request, 'gp_admin/index.html')


# Data Tables

def get_sis_students(request):
    sis_student_list = SIS_Student.objects.all()
    students = sis_student_list.filter(json__gender="M")
    student_json = [ s.json for s in sis_student_list ]
    return render(request, 'gp_admin/data_tables/get_sis_students.html', {
        'students': student_json,
        'total_students': len(student_json)
    })

class Get_Students(View):
    def get(self, request, *args, **kwargs):
        students = Student.objects.all()

        return render(request, 'gp_admin/data_tables/get_students.html', {
            'students': students,
            'total_students': len(students)
        })


class Edit_Student(View):
    stud_form = Student_Form

    def get(self, request, *args, **kwargs):
        stud = api.get_student(kwargs.get('student_number'))
        return render(request, 'gp_admin/data_tables/edit_student.html', {
            'stud': stud,
            'form': self.stud_form(instance=stud),
            'info': {
                'btn_label': 'Update',
                'href': reverse('gp_admin:get_students'),
                'type': 'edit',
                'path': 'students'
            }
        })
    
    def post(self, request, *args, **kwargs):
        stud = api.get_student(kwargs.get('student_number'))
        form = self.stud_form(request.POST, instance=stud)
        if form.is_valid():
            res = form.save()
            if res:
                messages.success(request, 'Success! Student ({0}, Student #: {1}) updated'.format(stud.get_full_name(), stud.student_number))
                return redirect('gp_admin:get_students')
            else:
                messages.error(request, 'An error occurred while updating data.')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors) )
        return redirect('gp_admin:edit_student')


class Get_Professors(View):
    def get(self, request, *args, **kwargs):
        prof_list =  api.get_professors()

        last_name_q = request.GET.get('last_name')
        first_name_q = request.GET.get('first_name')
        email_q = request.GET.get('email')

        if bool(last_name_q):
            prof_list = prof_list.filter(last_name__icontains=last_name_q)
        if bool(first_name_q):
            prof_list = prof_list.filter(first_name__icontains=first_name_q)
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

        for prof in professors:
            print(prof.id, prof.get_full_name(), prof.graduate_supervision_set.count())

        return render(request, 'gp_admin/data_tables/get_professors.html', {
            'professors': professors,
            'total_professors': len(prof_list)
        })

    def post(self, request, *args, **kwargs):
        pass


class Edit_Professor(View):
    prof_form = Professor_Form

    def get(self, request, *args, **kwargs):
        prof = api.get_professor(kwargs.get('username'), 'username')
        return render(request, 'gp_admin/data_tables/edit_professor.html', {
            'prof': prof,
            'form': self.prof_form(data=None, instance=prof.profile),
            'info': {
                'btn_label': 'Update',
                'href': reverse('gp_admin:get_professors'),
                'type': 'edit',
                'path': 'professors'
            }
        })

    def post(self, request, *args, **kwargs):
        prof = api.get_professor(kwargs.get('username'), 'username')
        form = self.prof_form(request.POST, instance=prof.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success! Professor ({0}, CWL: {1}) updated'.format(prof.get_full_name(), prof.username))
            return redirect('gp_admin:get_professors')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors) )
        return redirect('gp_admin:edit_professor')


class Get_Grad_Supervision(View):
    def get(self, request, *args, **kwargs):
        professors = api.get_professors()

        return render(request, 'gp_admin/data_tables/get_grad_supervision.html', {
            'professors': professors,
            'total_professors': len(professors)
        })


class Add_Grad_Supervision(View):
    form = Grad_Supervision_Form
    def get(self, request, *args, **kwargs):
        prof = api.get_professor(kwargs.get('username'), 'username')
        return render(request, 'gp_admin/data_tables/add_grad_supervision.html', {
            'prof': prof,
            'form': self.form,
            'prof_roles': Professor_Role.objects.all()
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
        return HttpResponseRedirect(reverse('gp_admin:add_grad_supervision', args=[kwargs.get('username')]))


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
    return HttpResponseRedirect(reverse('gp_admin:add_grad_supervision', args=[username]))


@require_http_methods(['POST'])
def delete_grad_supervision(request, username):
    gs = api.get_grad_supervision(request.POST.get('graduate_supervision'))
    if gs.delete():
        messages.success(request, 'Success! Graduate Supervision ({0} {1}) deleted.'.format(gs.student.first_name, gs.student.last_name))
    else:
        messages.error(request, 'An error occurred while deleting this graduate supervision.')
    return HttpResponseRedirect(reverse('gp_admin:edit_grad_supervision', args=[username]))


class Get_Comp_Exams2(View):
    # form_class = Comp_Exam_Form

    def get(self, request, *args, **kwargs):
        student_list = api.get_students()

        last_name_q = request.GET.get('last_name')
        first_name_q = request.GET.get('first_name')
        student_number_q = request.GET.get('student_number')
        email_q = request.GET.get('email')
        exam_date_q = request.GET.get('exam_date')

        if bool(last_name_q):
            student_list = student_list.filter(last_name__icontains=last_name_q)
        if bool(first_name_q):
            student_list = student_list.filter(first_name__icontains=first_name_q)
        if bool(student_number_q):
            student_list = student_list.filter(student_number__icontains=student_number_q)
        if bool(email_q):
            student_list = student_list.filter(email__icontains=email_q)
        if bool(exam_date_q):
            if exam_date_q == 'filled':
                student_list = student_list.exclude(comprehensive_exam__isnull=True)
            else:
                student_list = student_list.exclude(comprehensive_exam__isnull=False)


        page = request.GET.get('page', 1)
        paginator = Paginator(student_list, settings.PAGE_SIZE)

        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)

        reminders = Reminder.objects.all()
        for rem in reminders:
            print(rem.id, rem.months)

        for stud in Student.objects.all():
            pass
            # try:
            #     print(stud.id, stud.get_full_name(), stud.comprehensive_exam)
            # except Comprehensive_Exam.DoesNotExist:
            #     stud.comprehensive_exam = None

        return render(request, 'gp_admin/data_tables/get_comp_exams.html', {
            'students': students,
            'total_students': len(student_list),
            # 'form': self.form_class()
        })


    def post(self, request, *args, **kwargs):
        pass



class Get_Comp_Exams(View):
    def get(self, request, *args, **kwargs):
        today = datetime.today().date()
        students = api.get_students()
        reminders = api.get_reminders()
        for stud in students:
            expect_send_reminders = []
            for rem in reminders:
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
        users = api.get_users()

        return render(request, 'gp_admin/users/get_users.html', {
            'users': users,
            'total_users': len(users)
        })

    def post(self, request, *args, **kwargs):
        pass


class Add_User(View):
    user_form = User_Form
    profile_form = Profile_Form

    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/users/add_edit_user.html', {
            'users': api.get_users(),
            'user_form': self.user_form(),
            'profile_form': self.profile_form(),
            'info': {
                'btn_label': 'Create',
                'href': reverse('gp_admin:add_user'),
                'type': 'add',
                'path': 'users'
            }
        })

    def post(self, request, *args, **kwargs):
        user_form = self.user_form(request.POST)
        profile_form = self.profile_form(request.POST)

        errors = []
        if not user_form.is_valid():
            errors.append( api.get_error_messages(user_form.errors.get_json_data()) )
        if not profile_form.is_valid():
            errors.append( api.get_error_messages(profile_form.errors.get_json_data()) )

        if len(errors) == 0:
            user = user_form.save()
            profile_data = profile_form.cleaned_data

            # Create a profile and add roles and programs if they exist
            profile = api.create_profile(user, profile_data)

            roles = profile_data.get('roles', None)
            if roles:
                profile.roles.add( *roles )

            programs = profile_data.get('programs', None)
            if programs:
                profile.programs.add( *programs )

            messages.success(request, 'Success! User ({0} {1}, CWL: {2}) created'.format(user.first_name, user.last_name, user.username))
            return redirect('gp_admin:get_users')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(' '.join(errors)) )

        return redirect('gp_admin:add_user')


class Edit_User(View):
    user_form = User_Form
    profile_form = Profile_Form

    def get(self, request, *args, **kwargs):
        user = api.get_user(kwargs.get('username'), 'username')
        profile = api.has_profile_created(user)

        return render(request, 'gp_admin/users/add_edit_user.html', {
            'user': user,
            'user_form': self.user_form(data=None, instance=user),
            'profile_form': self.profile_form(data=None, instance=profile),
            'info': {
                'btn_label': 'Update',
                'href': reverse('gp_admin:edit_user', args=[ kwargs['username'] ]),
                'type': 'edit'
            }
        })

    def post(self, request, *args, **kwargs):
        user = api.get_user(request.POST.get('user'))
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

        return redirect('gp_admin:edit_user')


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




# class Add_Professor(View):
#     prof_form = Professor_Form

#     def get(self, request, *args, **kwargs):
#         return render(request, 'gp_admin/data_tables/add_edit_professor.html', {
#             'professors': api.get_professors(),
#             'form': self.prof_form(),
#             'info': {
#                 'btn_label': 'Create',
#                 'href': reverse('gp_admin:add_professor'),
#                 'type': 'add',
#                 'path': 'professors'
#             }
#         })

#     def post(self, request, *args, **kwargs):
#         prof_form = self.prof_form(request.POST)

#         if len(errors) == 0:
#             prof = prof_form.save()
#             # profile_data = profile_form.cleaned_data

#             # Create a profile and add roles
#             # profile = Profile.objects.create(user_id=user.id, preferred_name=profile_data.get('preferred_name', None))
#             # profile.roles.add( *profile_data['roles'] )

#             messages.success(request, 'Success! Professor ({0} {1}, CWL: {2}) created'.format(prof.user.first_name, prof.user.last_name, prof.user.username))
#             return redirect('gp_admin:get_users')
#         else:
#             messages.error(request, 'An error occurred. Form is invalid. {0}'.format(' '.join(errors)) )

#         return redirect('gp_admin:add_user')

