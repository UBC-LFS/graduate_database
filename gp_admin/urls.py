from django.urls import path
from . import views

app_name = 'gp_admin'

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.GetUsers.as_view(), name='get_users'),

    path('professors/', views.GetProfessors.as_view(), name='get_professors'),
    path('professors/add/', views.AddProfessor.as_view(), name='add_professor'),

    path('students/', views.GetStudents.as_view(), name='get_students'),
    path('students/add/', views.AddStudent.as_view(), name='add_student'),
    

    path('graduate-supervision/', views.GetGradSupervision.as_view(), name='get_grad_supervision'),
    
    path('students/sis/', views.get_sis_students, name='get_sis_students'),
    
    path('comprehensive-exams/', views.GetCompExams.as_view(), name='get_comp_exams')
]