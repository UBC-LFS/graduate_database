from django.conf import settings
from django.http import Http404
from django.contrib.auth.models import User
from django.db.models import Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta, date
from urllib.parse import urlparse

import json
import hashlib
from .models import *


# Student

def get_students():
    ''' Get all students '''
    return Student.objects.all()


def get_student_by_id(id):
    try:
        return Student.objects.get(id=id)
    except Student.DoesNotExist:
        raise Http404


def get_student_by_sn(sn):
    try:
        return Student.objects.get(student_number=sn)
    except Student.DoesNotExist:
        raise Http404


def get_students_by_name(name):
    studs = Student.objects.filter( Q(first_name__icontains=name) | Q(last_name__icontains=name) ).distinct()
    return studs if studs.exists() else None


def get_sis_students_by_day(when):
    day = date.today()

    if when == 'yesterday':
        day -= timedelta(days=1)

    elif when == 'week_ago':
        week_ago = day - timedelta(days=7)
        created = Student.objects.filter(sis_created_on__range=[week_ago, day]).distinct()
        updated = Student.objects.filter(sis_updated_on__range=[week_ago, day], sis_updated_on__gt=F('sis_created_on')).distinct()
        
        return created, updated, week_ago

    created = Student.objects.filter(sis_created_on=day).distinct()
    updated = Student.objects.filter(sis_updated_on=day, sis_updated_on__gt=F('sis_created_on')).distinct()

    return created, updated, day


# Professor

def get_professors():
    ''' Get all professors '''
    return User.objects.filter(profile__roles__in=[get_role_by_slug('program-advisor-director'), get_role_by_slug('supervisor')]).order_by('last_name', 'first_name').distinct()


def get_professor_by_id(id):
    ''' Get a professor by id '''
    try:
        return User.objects.get(id=id)
    except User.DoesNotExist:
        raise Http404
    

def get_professor_by_username(username):
    ''' Get a professor by username'''
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404


# Program Supervision

def get_program_supervision_by_id(id):
    try:
        return Graduate_Supervision.objects.get(id=id)
    except Graduate_Supervision.DoesNotExist:
        raise Http404


def get_program_supervision_by_stud_id_and_prof_id(stud_id, prof_id):
    try:
        return Graduate_Supervision.objects.get(student__id=stud_id, professor__id=prof_id)
    except Graduate_Supervision.DoesNotExist:
        raise Http404


def get_reminders():
    return Reminder.objects.all()


def sent_reminders():
    return Sent_Reminder.objects.all()

def get_program_supervision_view(username):
    prof = get_professor_by_username(username)

    prof.is_program_advisor_director = False
    prof.colleages = None
    if prof.profile.roles.filter(slug='program-advisor-director').exists():
        prof.is_program_advisor_director = True
        programs = [program for program in prof.profile.programs.all()]
        prof.colleages = User.objects.filter( Q(profile__programs__in=programs) & Q(profile__roles__in=[get_role_by_slug('program-advisor-director'), get_role_by_slug('supervisor')]) ).exclude(id=prof.id).order_by('last_name', 'first_name').distinct()

    return prof

# User

def get_users():
    return User.objects.all().order_by('last_name', 'first_name')


def get_user_by_id(id):
    try:
        return User.objects.get(id=id)
    except User.DoesNotExist:
        raise Http404


def get_user_by_username(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404


def create_user(username, first_name, last_name):
    ''' Create a new user with roles '''

    user = User.objects.create(
        username = username,
        first_name = first_name,
        last_name = last_name
    )

    profile = create_profile(user)
    profile.roles.add( get_role_by_slug('guest') )

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

    if 'superadmin' in roles or 'admin' in roles:
        return '/admin/'

    elif 'program-advisor-director' in roles:
        return '/program-advisor-director/'

    elif 'supervisor' in roles:
        return '/supervisor/'

    return '/guest/'


def get_roles(user):
    ''' Add roles into an user '''

    roles = []
    for role in user.profile.roles.all():
        if role.slug == 'superadmin':
            roles.append('superadmin')

        elif role.slug == 'admin':
            roles.append('admin')

        elif role.slug == 'program-advisor-director':
            roles.append('program-advisor-director')

        elif role.slug == 'supervisor':
            roles.append('supervisor')

        elif role.slug == 'guest':
            roles.append('guest')

    return roles


def get_role_by_id(id):
    try:
        return Role.objects.get(id=id)
    except Role.DoesNotExist:
        raise Http404


def get_role_by_slug(slug):
    try:
        return Role.objects.get(slug=slug)
    except Role.DoesNotExist:
        raise Http404


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

def get_reminder_by_id(id):
    try:
        return Reminder.objects.get(id=id)
    except Reminder.DoesNotExist:
        raise Http404


def get_reminder_by_slug(slug):
    try:
        return Reminder.objects.get(slug=slug)
    except Reminder.DoesNotExist:
        raise Http404


# Preparation

def get_status_by_id(id):
    ''' Get a status by id '''
    try:
        return Status.objects.get(id=id)
    except Status.DoesNotExist:
        raise Http404


def get_status_by_slug(slug):
    ''' Get a status by slug '''
    try:
        return Status.objects.get(slug=slug)
    except Status.DoesNotExist:
        raise Http404


def get_degree_by_id(id):
    ''' Get a degree by id '''
    try:
        return Degree.objects.get(id=id)
    except Degree.DoesNotExist:
        raise Http404


def get_degree_by_slug(slug):
    ''' Get a degree by slug '''
    try:
        return Degree.objects.get(slug=slug)
    except Degree.DoesNotExist:
        raise Http404


def get_program_by_id(id):
    ''' Get a program by id '''
    try:
        return Program.objects.get(id=id)
    except Program.DoesNotExist:
        raise Http404


def get_program_by_slug(slug):
    ''' Get a program by slug '''
    try:
        return Program.objects.get(slug=slug)
    except Program.DoesNotExist:
        raise Http404


def get_title_by_id(id):
    ''' Get a title by id '''
    try:
        return Title.objects.get(id=id)
    except Title.DoesNotExist:
        raise Http404


def get_title_by_slug(slug):
    ''' Get a title by slug '''
    try:
        return Title.objects.get(slug=slug)
    except Title.DoesNotExist:
        raise Http404


def get_position_by_id(id=id):
    ''' Get a position by id '''
    try:
        return Position.objects.get(id=id)
    except Position.DoesNotExist:
        raise Http404


def get_position_by_slug(slug):
    ''' Get a position by slug '''
    try:
        return Position.objects.get(slug=slug)
    except Position.DoesNotExist:
        raise Http404


def get_professor_role_by_id(id):
    ''' Get a professor role by id '''
    try:
        return Professor_Role.objects.get(id=id)
    except User.DoesNotExist:
        raise Http404


def get_professor_role_by_slug(slug):
    ''' Get a professor role by slug '''
    try:
        return Professor_Role.objects.get(slug=slug)
    except User.DoesNotExist:
        raise Http404


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


def build_tab_url(path, tab):
    return "{0}?t={1}".format(path, tab)


def build_new_tab_url(full_path, tab):
    if '&t=' in full_path:
        spl = full_path.split('&t=')
        return "{0}&t={1}".format(spl[0], tab)
    
    return "{0}&t={1}".format(full_path, tab)


def build_next_tab_url(path, next, tab):
    return "{0}?next={1}&t={2}".format(path, next, tab)


def build_new_next(request):
    full_path = request.get_full_path()
    next = urlparse(full_path)
    query = ''
    if len(next.query) > 0:
        for q in next.query.split('&'):
            arr = q.split('=')
            if len(arr[1]) > 0:
                if len(query) > 0:
                    query += '&'
                query += arr[0] + '=' + arr[1]

    new_next = next.path
    if len(query) > 0: new_next += '?' + query
    return new_next


def get_next(request):
    full_path = request.get_full_path()
    next = urlparse(full_path)
    return next.query.split('&p=')[0][5:]


def trim_tab(next):
    if '&t=' in next:
        spl = next.split('&t=')
        return spl[0]
    return next
