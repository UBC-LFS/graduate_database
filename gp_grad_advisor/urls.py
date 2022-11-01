from django.urls import path
from . import views

app_name = 'gp_grad_advisor'

urlpatterns = [
    path('', views.index, name='index'),
    path('graduate-supervision/', views.GetGradSupervision.as_view(), name='get_grad_supervision')
]
