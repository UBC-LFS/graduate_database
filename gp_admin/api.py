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


def get_professor_by_username(username):
    ''' Get a professor by username '''
    return get_object_or_404(Professor, username=username)


def get_students():
    ''' Get all students '''
    return Student.objects.all()


def get_sis_students():
    ''' Get all sis students '''
    return SIS_Student.objects.all()



# Reminder

def get_reminder(arg, type='id'):
    if type == 'slug':
        return get_object_or_404(Reminder, slug=arg)
    return get_object_or_404(Reminder, id=arg)


# User



def create_user(username, first_name, last_name):
    ''' Create a new user with roles '''

    user = User.objects.create(
        username = username,
        first_name = first_name,
        last_name = last_name
    )

    profile = Profile.objects.create(user_id=user.id)
    profile.roles.add( get_role('Guest', 'name') )

    return user


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


def get_role(arg, type='id'):
    ''' Get a role by id '''
    if type == 'slug':
        return get_object_or_404(Role, slug=arg)
    elif type == 'name':
        return get_object_or_404(Role, name=arg)
    return get_object_or_404(Role, id=arg)


# Preparation

def get_status(arg, type='id'):
    ''' Get a status by id '''
    if type == 'slug':
        return get_object_or_404(Status, slug=arg)
    return get_object_or_404(Status, id=arg)

def get_title(arg, type='id'):
    ''' Get a title by id '''
    if type == 'slug':
        return get_object_or_404(Title, slug=arg)
    return get_object_or_404(Title, id=arg)

def get_position(arg, type='id'):
    ''' Get a position by id '''
    if type == 'slug':
        return get_object_or_404(Position, slug=arg)
    return get_object_or_404(Position, id=arg)

def get_professor_role(arg, type='id'):
    ''' Get a professor role by id '''
    if type == 'slug':
        return get_object_or_404(Professor_Role, slug=arg)
    return get_object_or_404(Professor_Role, id=arg)

def get_program(arg, type='id'):
    ''' Get a program by id '''
    if type == 'slug':
        return get_object_or_404(Program, slug=arg)
    return get_object_or_404(Program, id=arg)