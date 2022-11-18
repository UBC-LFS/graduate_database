from django.urls import path
from . import views

app_name = 'gp_program_advisor_director'

urlpatterns = [
    path('program_supervision/', views.Get_Program_Supervision.as_view(), name='get_program_supervision'),
    path('', views.index, name='index')
]
