from django.urls import path
from . import views

app_name = 'gp_program_advisor_director'

urlpatterns = [
    path('', views.index, name='index'),
    path('program_supervision/', views.GetGradSupervision.as_view(), name='get_program_supervision')
]
