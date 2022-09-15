from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.urls import reverse

import json

from .models import *
from .forms import *
from . import api

from scheduler import tasks


def index(request):
    # tasks.main()
    print( request.session.get('loggedin_user') )
    
    return render(request, 'gp_admin/index.html')


# Data Tables

class Get_Students(View):
    def get(self, request, *args, **kwargs):
        student_list = Student.objects.all()

        last_name_q = request.GET.get('last_name')
        first_name_q = request.GET.get('first_name')
        student_number_q = request.GET.get('student_number')
        email_q = request.GET.get('email')

        if bool(last_name_q):
            student_list = student_list.filter(last_name__icontains=last_name_q)
        if bool(first_name_q):
            student_list = student_list.filter(first_name__icontains=first_name_q)
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

        sis_student_ids = [ s.student_number for s in api.get_sis_students() ]
        if len(sis_student_ids) > 0:
            for s in students:
                if s.student_number in sis_student_ids:
                    s.sis_details = SIS_Student.objects.filter(student_number=s.student_number).first().json

        return render(request, 'gp_admin/data_tables/get_students.html', {
            'students': students,
            'total_students': len(student_list)
        })


class Add_Student(View):
    form_class = Student_Create_Form

    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/data_tables/add_student.html', {
            'students': api.get_students(),
            'form': self.form_class()
        })


class Get_Professors(View):
    def get(self, request, *args, **kwargs):
        professor_list =  api.get_professors()

        last_name_q = request.GET.get('last_name')
        first_name_q = request.GET.get('first_name')
        email_q = request.GET.get('email')

        if bool(last_name_q):
            professor_list = professor_list.filter(last_name__icontains=last_name_q)
        if bool(first_name_q):
            professor_list = professor_list.filter(first_name__icontains=first_name_q)
        if bool(email_q):
            professor_list = professor_list.filter(email__icontains=email_q)

        page = request.GET.get('page', 1)
        paginator = Paginator(professor_list, settings.PAGE_SIZE)

        try:
            professors = paginator.page(page)
        except PageNotAnInteger:
            professors = paginator.page(1)
        except EmptyPage:
            professors = paginator.page(paginator.num_pages)

        for prof in professors:
            print(prof.supervision_set.count())

        return render(request, 'gp_admin/data_tables/get_professors.html', {
            'professors': professors,
            'total_professors': len(professor_list)
        })

    def post(self, request, *args, **kwargs):
        pass


class Add_Professor(View):
    form_class = Professor_Form

    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/data_tables/add_professor.html', {
            'professors': api.get_professors(),
            'form': self.form_class()
        })
    
    def post(self, request, *args, **kwargs):
        pass


class Get_Grad_Supervision(View):
    def get(self, request, *args, **kwargs):
        professor_list = api.get_professors()

        supervisions = []
        non_supervisors = 0
        num_supervisors = 1
        for prof in professor_list:
            num_students = prof.supervision_set.count()
            if num_students > 0:
                prof_id = prof.id
                prof_full_name = prof.get_full_name()
                prof_title = prof.title.name
                prof_position = prof.position.name

                i = 0
                for sup in prof.supervision_set.all():
                    if i > 0:
                        prof_id = None
                        prof_full_name = None
                        prof_title = None
                        prof_position = None
                        non_supervisors += 1
                    i += 1

                    supervisions.append({
                        'prof_id': prof_id,
                        'prof_full_name': prof_full_name,
                        'prof_title': prof_title,
                        'prof_position': prof_position,
                        'num_students': num_students,
                        'prof_role': sup.professor_role.name,
                        'stud_full_name': sup.student.get_full_name(),
                        'stud_current_degree': sup.student.current_degree,
                        'stud_program_code': sup.student.program_code,
                        'created_on': sup.created_on,
                        'updated_on': sup.updated_on,
                        'num_supervisors': num_supervisors,
                        'odd_or_even': 'odd' if num_supervisors % 2 != 0 else 'even'
                    })
                num_supervisors += 1

        return render(request, 'gp_admin/data_tables/get_grad_supervision.html', {
            'supervisions': supervisions,
            'total_supervisions': num_supervisors
        })


class Get_Comp_Exams(View):
    form_class = Comp_Exam_Form

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

        # for stud in Student.objects.all():
        #     try:
        #         print(stud.id, stud.get_full_name(), stud.comprehensive_exam)
        #     except Comprehensive_Exam.DoesNotExist:
        #         stud.comprehensive_exam = None

        return render(request, 'gp_admin/data_tables/get_comp_exams.html', {
            'students': students,
            'total_students': len(student_list),
            'form': self.form_class()
        })


    def post(self, request, *args, **kwargs):
        pass


class Get_Exam_Reminders(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/data_tables/get_exam_reminders.html', {
            'reminders': Exam_Reminder.objects.all().order_by('-created_at')
        })

    def post(self, request, *args, **kwargs):
        pass




def get_sis_students(request):
    sis_student_list = SIS_Student.objects.all()
    students = sis_student_list.filter(json__gender="M")

    print(len(students))

    student_json = [ s.json for s in sis_student_list ]

    return render(request, 'gp_admin/data_tables/get_sis_students.html', {
        'students': student_json,
        'total_students': len(student_json)
    })


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
        return render(request, 'gp_admin/users/user.html', {
            'user_form': self.user_form(),
            'profile_form': self.profile_form(),
            'info': {
                'btn_label': 'Create',
                'href': reverse('gp_admin:add_user'),
                'type': 'add'
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

            # # Create a profile and add roles
            profile = Profile.objects.create(user_id=user.id, preferred_name=profile_data.get('preferred_name', None))
            profile.roles.add( *profile_data['roles'] )

            messages.success(request, 'Success! User ({0} {1}, CWL: {2}) created'.format(user.first_name, user.last_name, user.username))
            return redirect('gp_admin:get_users')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(' '.join(errors)) )

        return redirect('gp_admin:add_user')


class Edit_User(View):
    user_form = User_Form
    profile_form = Profile_Form

    def get(self, request, *args, **kwargs):
        user = api.get_user(kwargs['username'], 'username')
        profile = api.has_profile_created(user)

        return render(request, 'gp_admin/users/user.html', {
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
            messages.success(request, 'Success! User ({0} {1}, CWL: {2}) updated'.format(user.first_name, user.last_name, user.username))
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
    form_class = Reminder_Form

    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/preparation/get_reminders.html', {
            'reminders': Reminder.objects.all().order_by('id'),
            'form': self.form_class()
        })
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            res = form.save()
            if res:
                messages.success(request, 'Success! Reminder with Type: {0} and Month: {1} created'.format(res.type, res.month))
            else:
                messages.error(request, 'An error occurred while saving data.')
        else:
            messages.error(request, 'An error occurred. Form is invalid. {0}'.format(form.errors))

        return redirect('gp_admin:get_reminders')


class Edit_Reminder(View):
    form_class = Reminder_Form

    def get(self, request, *args, **kwargs):
        reminder = api.get_reminder(kwargs['slug'], 'slug')
        return render(request, 'gp_admin/preparation/edit_reminder.html', {
            'form': self.form_class(data=None, instance=reminder)
        })
    
    def post(self, request, *args, **kwargs):
        reminder = api.get_reminder(kwargs['slug'], 'slug')
        form = self.form_class(request.POST, instance=reminder)
        if form.is_valid():
            res = form.save()
            if res:
                messages.success(request, 'Success! Reminder with Type: {0} and Month: {1} updated'.format(res.type, res.month))
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