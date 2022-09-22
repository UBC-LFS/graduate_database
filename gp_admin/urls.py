from django.urls import path
from . import views

app_name = 'gp_admin'

urlpatterns = [
    path('', views.index, name='index'),

    # Data Tables

    path('students/', views.Get_Students.as_view(), name='get_students'),
    path('students/<str:student_number>/edit/', views.Edit_Student.as_view(), name='edit_student'),

    path('professors/', views.Get_Professors.as_view(), name='get_professors'),
    path('professors/<str:username>/edit/', views.Edit_Professor.as_view(), name='edit_professor'),
    # path('professor/add/', views.Add_Professor.as_view(), name='add_professor'),
    
    path('graduate-supervision/', views.Get_Grad_Supervision.as_view(), name='get_grad_supervision'),
    path('graduate-supervision/<str:username>/add/', views.Add_Grad_Supervision.as_view(), name='add_grad_supervision'),
    path('api/graduate-supervision/<str:username>/edit/', views.edit_grad_supervision, name='edit_grad_supervision'),
    path('api/graduate-supervision/<str:username>/delete/', views.delete_grad_supervision, name='delete_grad_supervision'),
    
    path('comprehensive-exams/', views.Get_Comp_Exams.as_view(), name='get_comp_exams'),
    path('reminders/sent/', views.Sent_Reminders.as_view(), name='sent_reminders'),

    # path('students/sis/', views.get_sis_students, name='get_sis_students'),


    # Users
    
    path('users/all/', views.Get_Users.as_view(), name='get_users'),
    path('users/<str:username>/edit/', views.Edit_User.as_view(), name='edit_user'),
    path('user/add/', views.Add_User.as_view(), name='add_user'),

    path('users/roles/', views.Get_Roles.as_view(), name='get_roles'),
    path('api/roles/<str:slug>/edit/', views.edit_role, name='edit_role'),
    path('api/role/delete/', views.delete_role, name='delete_role'),

    # Preparation
    
    path('preparation/statuses/', views.Get_Statuses.as_view(), name='get_statuses'),
    path('api/statuses/<str:slug>/edit/', views.edit_status, name='edit_status'),
    path('api/status/delete/', views.delete_status, name='delete_status'),

    path('preparation/degrees/', views.Get_Degrees.as_view(), name='get_degrees'),
    path('api/degrees/<str:slug>/edit/', views.edit_degree, name='edit_degree'),
    path('api/degree/delete/', views.delete_degree, name='delete_degree'),

    path('preparation/programs/', views.Get_Programs.as_view(), name='get_programs'),
    path('api/programs/<str:slug>/edit/', views.edit_program, name='edit_program'),
    path('api/program/delete/', views.delete_program, name='delete_program'),

    path('preparation/titles/', views.Get_Titles.as_view(), name='get_titles'),
    path('api/titles/<str:slug>/edit/', views.edit_title, name='edit_title'),
    path('api/title/delete/', views.delete_title, name='delete_title'),

    path('preparation/positions/', views.Get_Positions.as_view(), name='get_positions'),
    path('api/positions/<str:slug>/edit/', views.edit_position, name='edit_position'),
    path('api/position/delete/', views.delete_position, name='delete_position'),

    path('preparation/professor-roles/', views.Get_Professor_Roles.as_view(), name='get_professor_roles'),
    path('api/professor-roles/<str:slug>/edit/', views.edit_professor_role, name='edit_professor_role'),
    path('api/professor-role/delete/', views.delete_professor_role, name='delete_professor_role'),

    path('preparation/reminders/', views.Get_Reminders.as_view(), name='get_reminders'),
    path('preparation/reminders/<str:slug>/edit/', views.Edit_Reminder.as_view(), name='edit_reminder'),
    path('api/preparation/comprehensive-exams/reminder/delete/', views.delete_reminder, name='delete_reminder')
   
]