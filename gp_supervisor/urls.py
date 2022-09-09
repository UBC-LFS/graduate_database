from django.urls import path
from . import views

app_name = 'gp_supervisor'

urlpatterns = [
    path('', views.index, name='index')

]