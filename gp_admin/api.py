from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import *

ROLES = {
    'Superadmin': 1,
    'Admin': 2,
    'Supervisor': 3,
    'Guest': 4
}

def get_professors():
    ''' Get all professors '''
    return Professor.objects.all()


def get_students():
    ''' Get all students '''
    return Student.objects.all()


def get_sis_students():
    ''' Get all sis students '''
    return SIS_Student.objects.all()


# --- User Role ---

def get_user_role_by_name(name):
    ''' Get a role by name '''
    return get_object_or_404(User_Role, name=name)


def get_roles(user):
    ''' Add roles into an user '''

    roles = []
    for role in user.profile.roles.all():
        if role.name == 'Superadmin':
            roles.append('Superadmin')

        elif role.name == 'Admin':
            roles.append('Admin')

        elif role.name == 'Supervisor':
            roles.append('Supervisor')

        elif role.name == 'Guest':
            roles.append('Guest')

    return roles


# --- User ---

def create_user(username, first_name, last_name):
    ''' Create a new user with user roles '''

    user = User.objects.create(
        username = username,
        first_name = first_name,
        last_name = last_name
    )

    profile = profile.objects.create(user_id=user.id)
    user_profile.roles.add( get_user_role_by_name('Guest') )

    return user
