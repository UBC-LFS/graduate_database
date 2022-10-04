from django import forms
from datetime import datetime
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import *


# Data Table

class Student_Form(forms.ModelForm):
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
    completion_date = forms.DateField(
        required = False,
        widget = forms.widgets.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        label = 'Completion Date'
    )
    graduation_date = forms.DateField(
        required = False,
        widget = forms.widgets.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        label = 'Graduation Date'
    )
    comprehensive_exam_date = forms.DateField(
        required = False,
        widget = forms.widgets.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        label = 'Comprehensive Exam Date'
    )

    class Meta:
        model = Student
        fields = [
            'date_of_birth', 'phone', 'sin', 'loa_months', 'loa_details', 'policy_85', 
            'status', 'start_date', 'completion_date', 'graduation_date', 'comprehensive_exam_date',
            'previous_institution_1', 'degree_1', 'gpa_1', 'previous_institution_2', 'degree_2', 'gpa_2', 'previous_institution_3', 'degree_3', 'gpa_3',
            'thesis_title', 'funding_sources', 'total_funding_awarded', 'taships', 'current_role', 'note' 
        ]
        widgets = {
            'phone': forms.TextInput(attrs={ 'class': 'form-control' }),
            'sin': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'loa_months': forms.TextInput(attrs={ 'type':'number', 'class': 'form-control' }),
            'loa_details': forms.TextInput(attrs={ 'class': 'form-control' }),
            'previous_institution_1': forms.TextInput(attrs={ 'class': 'form-control' }),
            'degree_1': forms.TextInput(attrs={ 'class': 'form-control' }),
            'gpa_1': forms.TextInput(attrs={ 'class': 'form-control' }),
            'previous_institution_2': forms.TextInput(attrs={ 'class': 'form-control' }),
            'degree_2': forms.TextInput(attrs={ 'class': 'form-control' }),
            'gpa_2': forms.TextInput(attrs={ 'class': 'form-control' }),
            'previous_institution_3': forms.TextInput(attrs={ 'class': 'form-control' }),
            'degree_3': forms.TextInput(attrs={ 'class': 'form-control' }),
            'gpa_3': forms.TextInput(attrs={ 'class': 'form-control' }),
            'thesis_title': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'funding_sources': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'total_funding_awarded': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'taships': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'current_role': forms.TextInput(attrs={ 'class': 'form-control' }),
            'note': SummernoteWidget()
        }
        labels = {
            'sin': 'SIN',
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
            'phone': 'Maximum length is 20 characters.',
            'sin': 'Maximum length is 20 characters.',
            'loa_details': 'Maximum length is 150 characters.',
            'previous_institution_1': 'Maximum length is 150 characters.',
            'degree_1': 'Maximum characters: 50',
            'gpa_1': 'Maximum length is 20 characters.',
            'previous_institution_2': 'Maximum length is 150 characters.',
            'degree_2': 'Maximum characters: 50',
            'gpa_2': 'Maximum length is 20 characters.',
            'previous_institution_3': 'Maximum length is 150 characters.',
            'degree_3': 'Maximum characters: 50',
            'gpa_3': 'Maximum length is 20 characters.',
            'thesis_title': 'Maximum length is 150 characters.', 
            'funding_sources': 'Maximum length is 150 characters.', 
            'total_funding_awarded': 'Maximum length is 150 characters.', 
            'taships': 'Maximum length is 150 characters.', 
            'current_role': 'Maximum length is 150 characters.'
        }


class Grad_Supervision_Form(forms.ModelForm):
    class Meta:
        model = Graduate_Supervision
        fields = ['student', 'professor', 'professor_role']
        labels = {
            'professor_role': 'Professor Role'
        }
        widgets = {
            'professor': forms.HiddenInput()
        }

    def clean_student(self):
        data = self.cleaned_data['student']
        if not data: raise ValidationError('This field is required.')
        return data
    
    def clean_professor(self):
        data = self.cleaned_data['professor']
        if not data: raise ValidationError('This field is required.')
        return data

    def clean_professor_role(self):
        data = self.cleaned_data['professor_role']
        if not data: raise ValidationError('This field is required.')
        return data


class Student_Additional_Form(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['thesis_title', 'current_role', 'funding_sources', 'total_funding_awarded', 'taships']
        widgets = {

        }
        help_texts = {

        }



# class Comp_Exam_Form(forms.ModelForm):
#     today = datetime.now()

#     exam_date = forms.DateField(
#         required = False,
#         #widget=forms.SelectDateWidget(years=range(today.year - 10, today.year + 10)),
#         widget = forms.widgets.DateInput(attrs={'type': 'date', 'class':'form-control'}),
#         label = 'Exam Date'
#     )

#     class Meta:
#         model = Comprehensive_Exam
#         fields = ['exam_date', 'note']


# Users


class User_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'is_superuser', 'is_active']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'username': 'CWL',
            'is_superuser': 'Superuser Status'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={ 'required': True, 'class': 'form-control' }),
            'last_name': forms.TextInput(attrs={ 'required': True, 'class': 'form-control' }),
            'email': forms.EmailInput(attrs={ 'required': True, 'class': 'form-control' }),
            'username': forms.TextInput(attrs={ 'required': True, 'class': 'form-control' })
        }
        help_texts = {
            'first_name': 'Maximum length is 150 characters.',
            'last_name': 'Maximum length is 150 characters.',
            'email': 'Maximum length is 254 characters.',
            'username': 'This is a unique field. Maximum length is 150 characters.',
            'is_superuser': "This field is necessary for a Superadmin role."
        }

    def clean_last_name(self):
        data = self.cleaned_data['last_name']    
        if not data: raise ValidationError('This field is required.')
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']    
        if not data: raise ValidationError('This field is required.')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']    
        if not data: raise ValidationError('This field is required.')
        return data


class Profile_Form(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(
        required = True,
        queryset = Role.objects.all(),
        widget = forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Profile
        fields = ['preferred_name', 'roles']
        labels = {
            'preferred_name': 'Preferred Name'
        }
        widgets = {
            'preferred_name': forms.TextInput(attrs={ 'class': 'form-control' })
        }
        help_texts = {
            'preferred_name': 'Maximum length is 150 characters.'
        }

    def clean_roles(self):
        data = self.cleaned_data['roles']
        if not data: raise ValidationError('This field is required.')
        return data


class Professor_Form(forms.ModelForm):
    programs = forms.ModelMultipleChoiceField(
        required = False,
        queryset = Program.objects.all(),
        widget = forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Profile
        fields = ['title', 'position', 'programs', 'phone', 'fax', 'office']
        widgets = {
            'phone': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'fax': forms.TextInput(attrs={ 'class': 'form-control' }),
            'office': forms.TextInput(attrs={ 'class': 'form-control' })
        }
        help_texts = {
            'phone': 'Maximum length is 150 characters.',
            'fax': 'Maximum length is 150 characters.',
            'office': 'Maximum length is 150 characters.'
        }



# class Profile_Form(forms.ModelForm):
#     roles = forms.ModelMultipleChoiceField(
#         required = True,
#         queryset = Role.objects.all(),
#         widget = forms.CheckboxSelectMultiple(),
#     )

#     programs = forms.ModelMultipleChoiceField(
#         required = True,
#         queryset = Program.objects.all(),
#         widget = forms.CheckboxSelectMultiple(),
#     )

#     class Meta:
#         model = Profile
#         fields = ['preferred_name', 'roles', 'title', 'position', 'programs', 'phone', 'fax', 'office']
#         labels = {
#             'preferred_name': 'Preferred Name'
#         }
#         widgets = {
#             'preferred_name': forms.TextInput(attrs={ 'class': 'form-control' }),
#             'phone': forms.TextInput(attrs={ 'class': 'form-control' }), 
#             'fax': forms.TextInput(attrs={ 'class': 'form-control' }),
#             'office': forms.TextInput(attrs={ 'class': 'form-control' })
#         }
#         help_texts = {
#             'preferred_name': 'Maximum length is 150 characters.',
#             'phone': 'Maximum length is 150 characters.',
#             'fax': 'Maximum length is 150 characters.',
#             'office': 'Maximum length is 150 characters.'
#         }

#     def clean_roles(self):
#         data = self.cleaned_data['roles']
#         if not data: raise ValidationError('This field is required.')
#         return data


class Role_Form(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={ 'class':'form-control' })
        }
        help_texts = {
            'name': 'This is a required and unique field. Maximum length is 150 characters.',
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
            'name': 'This is a required and unique field. Maximum length is 150 characters.',
        }


class Degree_Form(forms.ModelForm):
    class Meta:
        model = Degree
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={ 'class':'form-control' }),
            'code': forms.TextInput(attrs={ 'class':'form-control' })
        }
        help_texts = {
            'name': 'This is a required and unique field. Maximum length is 150 characters.',
            'code': 'This is a required and unique field. Maximum length is 10 characters.',
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
            'name': 'This is a required and unique field. Maximum length is 150 characters.',
            'code': 'This is a required and unique field. Maximum length is 10 characters.',
        }


class Title_Form(forms.ModelForm):
    class Meta:
        model = Title
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={ 'class':'form-control' })
        }
        help_texts = {
            'name': 'This is a required and unique field. Maximum length is 150 characters.',
        }

class Position_Form(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={ 'class':'form-control' })
        }
        help_texts = {
            'name': 'This is a required and unique field. Maximum length is 150 characters.',
        }

class Professor_Role_Form(forms.ModelForm):
    class Meta:
        model = Professor_Role
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={ 'class':'form-control' })
        }
        help_texts = {
            'name': 'This is a required and unique field. Maximum length is 150 characters.',
        }


class Reminder_Form(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'message', 'type', 'months']
        widgets = {
            'title': forms.TextInput(attrs={ 'class':'form-control' }),
            'message': SummernoteWidget(),
            'type': forms.TextInput(attrs={ 'class':'form-control' }),
            'months': forms.TextInput(attrs={ 'class':'form-control' })
        }
        help_texts = {
            'title': 'This is a required field. Maximum length is 150 characters.',
            'message': 'This is a required field.',
            'type': 'This is a required and unique field. Maximum length is 150 characters.',
            'months': 'This is a required field. Must be numeric (Minimun value: 1, Maximum Value: 200)'
        }
