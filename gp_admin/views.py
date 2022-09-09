from django.conf import settings
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from .models import *
from .forms import *
from . import api

from scheduler import tasks


def index(request):
    print( request.session.get('loggedin_user') )
    
    return render(request, 'gp_admin/index.html')


class GetUsers(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all().order_by('last_name', 'first_name')

        return render(request, 'gp_admin/get_users.html', {
            'users': users,
            'total_users': len(users)
        })
    
    def post(self, request, *args, **kwargs):
        pass
    


class GetProfessors(View):
    def get(self, request, *args, **kwargs):
        # tasks.main()

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

        return render(request, 'gp_admin/get_professors.html', {
            'professors': professors,
            'total_professors': len(professor_list)
        })

    def post(self, request, *args, **kwargs):
        pass


class AddProfessor(View):
    form_class = ProfessorCreateForm

    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/add_professor.html', {
            'professors': api.get_professors(),
            'form': self.form_class()
        })




class GetStudents(View):
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

        return render(request, 'gp_admin/get_students.html', {
            'students': students,
            'total_students': len(student_list)
        })


class AddStudent(View):
    form_class = StudentCreateForm

    def get(self, request, *args, **kwargs):
        return render(request, 'gp_admin/add_student.html', {
            'students': api.get_students(),
            'form': self.form_class()
        })




class GetGradSupervision(View):
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

        return render(request, 'gp_admin/get_grad_supervision.html', {
            'supervisions': supervisions,
            'total_supervisions': num_supervisors
        })


class GetCompExams(View):
    form_class = CompExamForm

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

        return render(request, 'gp_admin/get_comp_exams.html', {
            'students': students,
            'total_students': len(student_list),
            'form': self.form_class()
        })


    def post(self, request, *args, **kwargs):
        pass




def get_sis_students(request):
    sis_student_list = SIS_Student.objects.all()
    students = sis_student_list.filter(json__gender="M")

    print(len(students))

    student_json = [ s.json for s in sis_student_list ]

    return render(request, 'gp_admin/get_sis_students.html', {
        'students': student_json,
        'total_students': len(student_json)
    })
