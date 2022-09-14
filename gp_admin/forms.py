from django import forms
from datetime import datetime
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import *


class Professor_Create_Form(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['last_name', 'first_name', 'title', 'position', 'program', 'email', 'phone', 'fax', 'office']
        widgets = {
            'last_name': forms.TextInput(attrs={ 'class': 'form-control' }),
            'first_name': forms.TextInput(attrs={ 'class': 'form-control' }),
            'email': forms.TextInput(attrs={ 'class': 'form-control' }),
            'phone': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'fax': forms.TextInput(attrs={ 'class': 'form-control' }),
            'office': forms.TextInput(attrs={ 'class': 'form-control' })
        }
        help_texts = {
            'last_name': 'Maximum characters: 150',
            'first_name': 'Maximum characters: 150',
            'email': 'This field is unique. Maximum characters: 254',
            'phone': 'Maximum characters: 150',
            'fax': 'Maximum characters: 150',
            'office': 'Maximum characters: 150'
        }


class Student_Create_Form(forms.ModelForm):
    date_of_birth = forms.DateField(
        required = False,
        widget = forms.widgets.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        label = 'Date of Birth'
    )

    start_date = forms.DateField(
        required = False,
        widget = forms.widgets.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        label = 'Start Date'
    )

    class Meta:
        model = Student
        fields = [
            'last_name', 'first_name', 'middle_name', 'student_number', 'email', 'gender', 'date_of_birth', 
            'phone_work', 'phone_home', 'address', 'city', 'province', 'postal_code', 'country', 'perm_address', 
            'foreign_domestic', 'sin', 'current_degree', 'program_code', 'status', 'start_date', 'loa_months', 'loa_details',
            'previous_institution_1', 'degree_1', 'gpa_1', 'previous_institution_2', 'degree_2', 'gpa_2', 'previous_institution_3',
            'degree_3', 'gpa_3', 'policy_85', 'note'
        ]
        widgets = {
            'last_name': forms.TextInput(attrs={ 'class': 'form-control' }),
            'first_name': forms.TextInput(attrs={ 'class': 'form-control' }),
            'middle_name': forms.TextInput(attrs={ 'class': 'form-control' }),
            'student_number': forms.TextInput(attrs={ 'class': 'form-control' }),
            'email': forms.TextInput(attrs={ 'class': 'form-control' }),
            'phone_work': forms.TextInput(attrs={ 'class': 'form-control' }),
            'phone_home': forms.TextInput(attrs={ 'class': 'form-control' }),
            'address': forms.TextInput(attrs={ 'class': 'form-control' }),
            'city': forms.TextInput(attrs={ 'class': 'form-control' }),
            'province': forms.TextInput(attrs={ 'class': 'form-control' }),
            'postal_code': forms.TextInput(attrs={ 'class': 'form-control' }),
            'country': forms.TextInput(attrs={ 'class': 'form-control' }),
            'perm_address': forms.TextInput(attrs={ 'class': 'form-control' }),
            'sin': forms.TextInput(attrs={ 'class': 'form-control' }),
            'current_degree': forms.TextInput(attrs={ 'class': 'form-control' }),
            'program_code': forms.TextInput(attrs={ 'class': 'form-control' }),
            'status': forms.TextInput(attrs={ 'class': 'form-control' }),
            'loa_months': forms.TextInput(attrs={ 'type':'number', 'class': 'form-control' }),
            'loa_details': forms.TextInput(attrs={ 'class': 'form-control' }),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
            'previous_institution_1': forms.TextInput(attrs={ 'class': 'form-control' }),
            'degree_1': forms.TextInput(attrs={ 'class': 'form-control' }),
            'gpa_1': forms.TextInput(attrs={ 'class': 'form-control' }),
            'previous_institution_2': forms.TextInput(attrs={ 'class': 'form-control' }),
            'degree_2': forms.TextInput(attrs={ 'class': 'form-control' }),
            'gpa_2': forms.TextInput(attrs={ 'class': 'form-control' }),
            'previous_institution_3': forms.TextInput(attrs={ 'class': 'form-control' }),
            'degree_3': forms.TextInput(attrs={ 'class': 'form-control' }),
            'gpa_3': forms.TextInput(attrs={ 'class': 'form-control' })
        }
        labels = {
            'last_name': 'Last Name',
            'first_name': 'First Name',
            'middle_name': 'Middle Name',
            'student_number': 'Student Number',
            'postal_code': 'Postal Code',
            'phone_work': 'Phone Number (Work)',
            'phone_home': 'Phone Number (Home)',
            'perm_address': 'Permanent Address',
            'foreign_domestic': 'Foreign/Domestic',
            'sin': 'SIN',
            'current_degree': 'Current Degree',
            'program_code': 'Program Code',
            'loa_months': 'LOA (Months)',
            'loa_details': 'LOA Details',
            'previous_institution_1': 'Previous Institution 1',
            'gpa_1': 'GPA 1',
            'previous_institution_2': 'Previous Institution 2',
            'gpa_2': 'GPA 2',
            'previous_institution_3': 'Previous Institution 3',
            'gpa_3': 'GPA 3',
        }
        help_texts = {
            'last_name': 'Maximum characters: 150',
            'first_name': 'Maximum characters: 150',
            'middle_name': 'Maximum characters: 150',
            'student_number': 'Maximum characters: 8',
            'email': 'This field is unique. Maximum characters: 150',
            'phone_work': 'Maximum characters: 20',
            'phone_home': 'Maximum characters: 20',
            'address': 'Maximum characters: 150',
            'city': 'Maximum characters: 150',
            'province': 'Maximum characters: 150',
            'postal_code': 'Maximum characters: 20',
            'country': 'Maximum characters: 150',
            'perm_address': 'Maximum characters: 150',
            'sin': 'Maximum characters: 20',
            'current_degree': 'Maximum characters: 150',
            'program_code': 'Maximum characters: 20',
            'status': 'Maximum characters: 150',
            'loa_details': 'Maximum characters: 150',
            'previous_institution_1': 'Maximum characters: 150',
            'degree_1': 'Maximum characters: 50',
            'gpa_1': 'Maximum characters: 20',
            'previous_institution_2': 'Maximum characters: 150',
            'degree_2': 'Maximum characters: 50',
            'gpa_2': 'Maximum characters: 20',
            'previous_institution_3': 'Maximum characters: 150',
            'degree_3': 'Maximum characters: 50',
            'gpa_3': 'Maximum characters: 20'
        }


class Comp_Exam_Form(forms.ModelForm):
    today = datetime.now()

    exam_date = forms.DateField(
        required = False,
        #widget=forms.SelectDateWidget(years=range(today.year - 10, today.year + 10)),
        widget = forms.widgets.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        label = 'Exam Date'
    )

    class Meta:
        model = Comprehensive_Exam
        fields = ['exam_date', 'note']


# Users


class Role_Form(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={ 'class':'form-control' })
        }
        help_texts = {
            'name': 'This is a required and unique field. Maximum characters: 150',
        }


# Preparation

class Status_Form(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={ 'class':'form-control' })
        }
        help_texts = {
            'name': 'This is a required and unique field. Maximum characters: 150',
        }

class Title_Form(forms.ModelForm):
    class Meta:
        model = Title
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={ 'class':'form-control' })
        }
        help_texts = {
            'name': 'This is a required and unique field. Maximum characters: 150',
        }

class Position_Form(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={ 'class':'form-control' })
        }
        help_texts = {
            'name': 'This is a required and unique field. Maximum characters: 150',
        }

class Professor_Role_Form(forms.ModelForm):
    class Meta:
        model = Professor_Role
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={ 'class':'form-control' })
        }
        help_texts = {
            'name': 'This is a required and unique field. Maximum characters: 150',
        }


class Program_Form(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={ 'class':'form-control' }),
            'code': forms.TextInput(attrs={ 'class':'form-control' })
        }
        help_texts = {
            'name': 'This is a required and unique field. Maximum characters: 150',
            'code': 'This is a required and unique field. Maximum characters: 10',
        }


class Reminder_Form(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'message', 'type', 'month']
        widgets = {
            'title': forms.TextInput(attrs={ 'class':'form-control' }),
            'message': SummernoteWidget(),
            'type': forms.TextInput(attrs={ 'class':'form-control' }),
            'month': forms.TextInput(attrs={ 'class':'form-control' })
        }
        help_texts = {
            'title': 'This is a required field. Maximum characters: 150',
            'message': 'This is a required field.',
            'type': 'This is a required and unique field. Maximum characters: 150',
            'month': 'This is a required field. Must be numeric (Minimun value: 1, Maximum Value: 200)'
        }
