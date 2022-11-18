from django.urls import path
from . import views

app_name = 'gp_supervisor'

urlpatterns = [
    path('', views.index, name='index'),
    path('graduate_supervision/', views.Get_Grad_Supervision.as_view(), name='get_grad_supervision'),
]
