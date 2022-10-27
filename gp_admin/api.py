from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import hashlib
from .models import *


# Student

def get_students():
    ''' Get all students '''
    return Student.objects.all()

def get_student(arg):
    try:
        return Student.objects.get(student_number=arg)
    except Student.DoesNotExist:
        raise Http404


# Professor

def get_professors(program=None):
    ''' Get all professors '''
    if program is not None:
        pass
    return User.objects.filter(profile__roles__in=[get_role('graduate-advisor', 'slug'), get_role('supervisor', 'slug')]).order_by('last_name', 'first_name')


def get_professor(arg, type='id'):
    ''' Get a professor '''
    if type == 'username':
        return get_object_or_404(User, username=arg)
    return get_object_or_404(User, id=arg)


# Graduate Supervision

def get_grad_supervision(arg, type='id'):
    return get_object_or_404(Graduate_Supervision, id=arg)


def get_reminders():
    return Reminder.objects.all()


def sent_reminders():
    return Sent_Reminder.objects.all()

# User

def get_users():
    return User.objects.all().order_by('last_name', 'first_name')


def get_user(arg, type='id'):
    if type == 'username':
        return get_object_or_404(User, username=arg)
    return get_object_or_404(User, id=arg)


def create_user(username, first_name, last_name):
    ''' Create a new user with roles '''

    user = User.objects.create(
        username = username,
        first_name = first_name,
        last_name = last_name
    )

    profile = create_profile(user)
    profile.roles.add( get_role('Guest', 'name') )

    return user

def create_profile(user):
    return Profile.objects.create(user_id=user.id)


def has_profile_created(user):
    ''' Check an user has a profile '''
    try:
        return user.profile
    except Profile.DoesNotExist:
        return create_profile(user)


def redirect_to_index_page(roles):
    ''' Redirect to an index page given roles '''

    if 'Superadmin' in roles or 'Admin' in roles:
        return '/admin/'

    elif 'Graduate Advisor' in roles:
        return '/gradudate-advisor/'    

    elif 'Supervisor' in roles:
        return '/supervisor/'
    
    return '/guest/'


def get_roles(user):
    ''' Add roles into an user '''

    roles = []
    for role in user.profile.roles.all():
        if role.name == 'Superadmin':
            roles.append('Superadmin')

        elif role.name == 'Admin':
            roles.append('Admin')

        elif role.name == 'Graduate Advisor':
            roles.append('Graduate Advisor')

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


# def update_profile_roles(profile, old_roles, data):
#     ''' Update roles of a user '''

#     if check_two_querysets_equal( old_roles, data.get('roles') ) == False:
#         profile.roles.remove( *old_roles ) # Remove current roles
#         new_roles = list( data.get('roles') )
#         profile.roles.add( *new_roles )  # Add new roles

#     return True if profile.roles else False


# def check_two_querysets_equal(qs1, qs2):
#     ''' Helper funtion: To check whether two querysets are equal or not '''
#     if len(qs1) != len(qs2):
#         return False

#     d = dict()
#     for qs in qs1:
#         item = qs.name.lower()
#         if item in d.keys(): d[item] += 1
#         else: d[item] = 1

#     for qs in qs2:
#         item = qs.name.lower()
#         if item in d.keys(): d[item] += 1
#         else: d[item] = 1

#     for k, v in d.items():
#         if v != 2: return False
#     return True


# Reminder

def get_reminder(arg, type='id'):
    if type == 'slug':
        return get_object_or_404(Reminder, slug=arg)
    return get_object_or_404(Reminder, id=arg)


# Preparation

def get_status(arg, type='id'):
    ''' Get a status by id '''
    if type == 'slug':
        return get_object_or_404(Status, slug=arg)
    return get_object_or_404(Status, id=arg)


def get_degree(arg, type='id'):
    ''' Get a degree by id '''
    if type == 'slug':
        return get_object_or_404(Degree, slug=arg)
    return get_object_or_404(egree, id=arg)


def get_program(arg, type='id'):
    ''' Get a program by id '''
    if type == 'slug':
        return get_object_or_404(Program, slug=arg)
    return get_object_or_404(Program, id=arg)



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


def get_filtered_items(request, all_list, path):

    first_name_q = request.GET.get('first_name')
    last_name_q = request.GET.get('last_name')
    cwl_q = request.GET.get('cwl')
    email_q = request.GET.get('email')

    if bool(first_name_q):
        all_list = all_list.filter(first_name__icontains=first_name_q)
    if bool(last_name_q):
        all_list = all_list.filter(last_name__icontains=last_name_q)
    if bool(cwl_q):
        all_list = all_list.filter(username__icontains=cwl_q)
    if bool(email_q):
        all_list = all_list.filter(email__icontains=email_q)

    page = request.GET.get('page', 1)
    paginator = Paginator(all_list, settings.PAGE_SIZE)
    # paginator = Paginator(all_list, 2)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    
    if path == 'users':
        pass
    
    return items


# Session


def remove_session(session):
    ''' Delete forms in session if they exist '''

    print(session.keys())
    if 'basic_info_form' in session:
        del session['basic_info_form']
    
    if 'additional_info_form' in session:
        del session['additional_info_form']
    
    if 'previous_school_info_form' in session:
        del session['previous_school_info_form']
    
    print(session.keys())



# Helper functions

def make_hash(data):
    return hashlib.sha256( json.dumps(data).encode('utf-8') ).hexdigest()


def build_url(path, next_path, tab):
    return "{0}?next={1}&t={2}".format(path, next_path, tab)


def get_error_messages(errors):
    messages = ''
    for key in errors.keys():
        value = errors[key]
        messages += key.replace('_', ' ').upper() + ': ' + value[0]['message'] + ' '
    return messages.strip()


def split_capitalize(s):
    words = [ word.capitalize() for word in s.split('_') ]
    return ' '.join(words)


def queryset_to_dict(post):
    data = {}
    for key, value in dict(post).items():
        if key not in ['current_page', 'next', 'tab', 'save']:
            data[key] = value if key in ['roles', 'programs'] else value[0]    
    return data



# ROLES = {
#     'Superadmin': 1,
#     'Admin': 2,
#     'Supervisor': 3,
#     'Guest': 4
# }