from django.conf import settings
from django.test import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse
from urllib.parse import urlencode

from gp_admin import api


LOGIN_URL = '/accounts/local_login/'
ContentType = 'application/x-www-form-urlencoded'

DATA = [
    'gp_admin/fixtures/degrees.json',
    'gp_admin/fixtures/graduate_supervisions.json',
    'gp_admin/fixtures/positions.json',
    'gp_admin/fixtures/professor_roles.json',
    'gp_admin/fixtures/profile_programs.json',
    'gp_admin/fixtures/profile_roles.json',
    'gp_admin/fixtures/profiles.json',
    'gp_admin/fixtures/programs.json',
    'gp_admin/fixtures/reminders.json',
    'gp_admin/fixtures/roles.json',
    'gp_admin/fixtures/sent_reminders.json',
    'gp_admin/fixtures/statuses.json',
    'gp_admin/fixtures/students.json',
    'gp_admin/fixtures/titles.json',
    'gp_admin/fixtures/users.json'
]

USERS = ['user1.prof', 'test.guest1']
USER_IDS = [3, 9]

PASSWORD = 'password'


NEXT = '/admin/users/all/?page=1'

class UserTest(TestCase):
    fixtures = DATA

    @classmethod
    def setUpTestData(cls):
        #print('\User testing has started ==>')
        cls.user = api.get_user(USERS[0], 'username')

    def login(self, username=None, password=None):
        if username and password:
            self.client.post(LOGIN_URL, data={'username': username, 'password': password})
        else:
            self.client.post(LOGIN_URL, data={'username': self.user.username, 'password': PASSWORD})

    def messages(self, res):
        return [m.message for m in get_messages(res.wsgi_request)]
    
    '''def test_get_users(self):
        print('- Test: get users')

        self.login()
        res = self.client.get( reverse('gp_admin:get_users') )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context['users']), 9)
        self.assertEqual(res.context['total_users'], 9)

    def test_create_user_tab_error(self):
        print('- Test: create an user - tab error')
        self.login()

        TAB = 'basic_infoa'
        CURRENT_PAGE = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB)
    
        user_profile_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'is_superuser': '',
            'is_active': 'on',
            'preferred_name': 'preferred name',
            'roles': ['4'],
            'phone': '',
            'office': '',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(user_profile_form, True), content_type=ContentType)
        self.assertEqual(res.status_code, 404)'''


    '''def test_create_user_missing_required_fields_firstname(self):
        print('- Test: create an user - missing required fields - first name')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB)
        
        user_profile_form = {
            'first_name': '',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'is_superuser': 'on',
            'is_active': 'on',
            'preferred_name': 'preferred name',
            'roles': ['1', '2'],
            'phone': '',
            'office': '',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(user_profile_form, True), content_type=ContentType)
        messages = self.messages(res) 
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. FIRST NAME: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)


    def test_create_user_missing_required_fields_lastname(self):
        print('- Test: create an user - missing required fields - last name')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB)

        user_profile_form = {
            'first_name': 'firstname',
            'last_name': '',
            'email': 'email@example.com',
            'username': 'username',
            'is_superuser': 'on',
            'is_active': 'on',
            'preferred_name': 'preferred name',
            'roles': ['1'],
            'phone': '',
            'office': '',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(user_profile_form, True), content_type=ContentType)
        messages = self.messages(res) 
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. LAST NAME: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)


    def test_create_user_missing_required_fields_email(self):
        print('- Test: create an user - missing required fields - email')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB)

        user_profile_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': '',
            'username': 'username',
            'is_superuser': 'on',
            'is_active': 'on',
            'preferred_name': 'preferred name',
            'roles': ['1'],
            'phone': '',
            'office': '',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(user_profile_form, True), content_type=ContentType)
        messages = self.messages(res) 
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. EMAIL: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)


    def test_create_user_missing_required_fields_username(self):
        print('- Test: create an user - missing required fields - username')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB)

        user_profile_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': '',
            'is_superuser': 'on',
            'is_active': 'on',
            'preferred_name': 'preferred name',
            'roles': ['1'],
            'phone': '',
            'office': '',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(user_profile_form, True), content_type=ContentType)
        messages = self.messages(res) 
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. USERNAME: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)

    def test_create_user_missing_required_fields_roles(self):
        print('- Test: create an user - missing required fields - roles')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB)

        user_profile_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'is_superuser': 'on',
            'is_active': 'on',
            'preferred_name': 'preferred name',
            'roles': [],
            'phone': '',
            'office': '',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(user_profile_form, True), content_type=ContentType)
        messages = self.messages(res) 
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. ROLES: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)


    # user profile form
    def test_create_user_profile_form_only(self):
        print('- Test: create an user - user profile form only')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB)

        user_profile_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'is_superuser': '',
            'is_active': 'on',
            'preferred_name': 'preferred name',
            'roles': ['4'],
            'phone': '',
            'office': '',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(user_profile_form, True), content_type=ContentType)
        messages = self.messages(res) 
        self.assertEqual(messages[0], 'Success! User (firstname lastname, CWL: username) created.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)

        user = api.get_user(user_profile_form['username'], 'username')
        self.assertEqual(user.first_name, user_profile_form['first_name'])
        self.assertEqual(user.last_name, user_profile_form['last_name'])
        self.assertEqual(user.email, user_profile_form['email'])
        self.assertEqual(user.username, user_profile_form['username'])
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.profile.preferred_name, user_profile_form['preferred_name'])
        self.assertEqual(user.profile.roles.count(), len(user_profile_form['roles']))

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, user_profile_form['roles'])

        self.assertIsNone(user.profile.title)
        self.assertIsNone(user.profile.position)
        self.assertIsNone(user.profile.phone)
        self.assertIsNone(user.profile.office)
        self.assertEqual(user.profile.programs.count(), 0)'''


    '''def test_create_user_profile_form_success1(self):
        print('- Test: create an user - user profile form - success1 [3,4] [1,2]')
        self.login()

        
        TAB1 = 'role_details'
        CURRENT_PAGE1 = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB1)

        prof_form = {
            'title': '1',
            'position': '3',
            'programs': ['1','2'],
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1,
            'save': 'Save'
        }

        res1 = self.client.post(reverse('gp_admin:create_user'), data=urlencode(prof_form, True), content_type=ContentType, follow=True)
        messages1 = self.messages(res1)
        self.assertEqual(messages1[0], 'Success! Role Details Form saved.')
        self.assertEqual(res1.status_code, 200)

        TAB2 = 'basic_info'
        CURRENT_PAGE2 = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB2)

        user_profile_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'is_superuser': 'on',
            'is_active': 'on',
            'preferred_name': 'preferred name',
            'roles': ['3','4'],
            'phone': 'phone',
            'office': 'office',
            'current_page': CURRENT_PAGE2,
            'next': NEXT,
            'tab': TAB2
        }

        res2 = self.client.post(reverse('gp_admin:create_user'), data=urlencode(user_profile_form, True), content_type=ContentType, follow=True)
        messages2 = self.messages(res2)
        self.assertEqual(messages2[0], 'Success! User (firstname lastname, CWL: username) created.')
        self.assertEqual(res2.status_code, 200)

        user = api.get_user(user_profile_form['username'], 'username')
        self.assertEqual(user.first_name, user_profile_form['first_name'])
        self.assertEqual(user.last_name, user_profile_form['last_name'])
        self.assertEqual(user.email, user_profile_form['email'])
        self.assertEqual(user.username, user_profile_form['username'])
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.profile.phone, user_profile_form['phone'])
        self.assertEqual(user.profile.office, user_profile_form['office'])
        self.assertEqual(user.profile.preferred_name, user_profile_form['preferred_name'])
        self.assertEqual(user.profile.roles.count(), len(user_profile_form['roles']))

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, user_profile_form['roles'])

        self.assertEqual(user.profile.title.id, int(prof_form['title']))
        self.assertEqual(user.profile.position.id, int(prof_form['position']))
        self.assertEqual(user.profile.programs.count(), len(prof_form['programs']))

        programs = [ str(program.id) for program in user.profile.programs.all() ]
        self.assertEqual(programs, prof_form['programs'])


    def test_create_user_profile_form_success2(self):
        print('- Test: create an user - user profile form with different data - success [3,4] [1,2]')
        self.login()

        TAB1 = 'basic_info'
        CURRENT_PAGE1 = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB1)

        user_profile_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'is_superuser': 'on',
            'is_active': 'on',
            'preferred_name': 'preferred name',
            'roles': ['3', '4'],
            'phone': 'phone',
            'office': 'office',
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1,
            'save': 'Save'
        }

        res1 = self.client.post(reverse('gp_admin:create_user'), data=urlencode(user_profile_form, True), content_type=ContentType, follow=True)
        messages1 = self.messages(res1)
        self.assertEqual(messages1[0], 'Success! Basic Information Form saved.')
        self.assertEqual(res1.status_code, 200)

        TAB2 = 'role_details'
        CURRENT_PAGE2 = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB2)

        prof_form = {
            'title': '1',
            'position': '3',
            'programs': ['1','2'],
            'current_page': CURRENT_PAGE2,
            'next': NEXT,
            'tab': TAB2,
            'save': 'Save'
        }

        res2 = self.client.post(reverse('gp_admin:create_user'), data=urlencode(prof_form, True), content_type=ContentType, follow=True)
        messages2 = self.messages(res2)
        self.assertEqual(messages2[0], 'Success! Role Details Form saved.')
        self.assertEqual(res2.status_code, 200)

        data = {
            'first_name': 'firstname2',
            'last_name': 'lastname2',
            'email': 'email2@example.com',
            'username': 'username2',
            'is_superuser': '',
            'is_active': '',
            'preferred_name': 'preferred name2',
            'roles': ['1'],
            'phone': '',
            'office': '',
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(data, True), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User (firstname2 lastname2, CWL: username2) created.')
        self.assertEqual(res.status_code, 200)

        user = api.get_user(data['username'], 'username')
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.username, data['username'])
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_active)
        self.assertIsNone(user.profile.phone)
        self.assertIsNone(user.profile.office)
        self.assertEqual(user.profile.preferred_name, data['preferred_name'])
        self.assertEqual(user.profile.roles.count(), len(data['roles']))

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, data['roles'])

        self.assertEqual(user.profile.title.id, int(prof_form['title']))
        self.assertEqual(user.profile.position.id, int(prof_form['position']))
        self.assertEqual(user.profile.programs.count(), len(prof_form['programs']))

        programs = [ str(program.id) for program in user.profile.programs.all() ]
        self.assertEqual(programs, prof_form['programs'])
    

    def test_create_user_prof_form_success3(self):
        print('- Test: create an user - prof form with different data - success [3,4] []')
        self.login()

        TAB1 = 'basic_info'
        CURRENT_PAGE1 = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB1)

        user_profile_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'is_superuser': 'on',
            'is_active': 'on',
            'preferred_name': 'preferred name',
            'roles': ['3', '4'],
            'phone': 'phone',
            'office': 'office',
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1,
            'save': 'Save'
        }

        res1 = self.client.post(reverse('gp_admin:create_user'), data=urlencode(user_profile_form, True), content_type=ContentType, follow=True)
        messages1 = self.messages(res1)
        self.assertEqual(messages1[0], 'Success! Basic Information Form saved.')
        self.assertEqual(res1.status_code, 200)

        TAB2 = 'role_details'
        CURRENT_PAGE2 = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB2)

        prof_form = {
            'title': '1',
            'position': '3',
            'programs': ['1','2'],
            'current_page': CURRENT_PAGE2,
            'next': NEXT,
            'tab': TAB2,
            'save': 'Save'
        }

        res2 = self.client.post(reverse('gp_admin:create_user'), data=urlencode(prof_form, True), content_type=ContentType, follow=True)
        messages2 = self.messages(res2)
        self.assertEqual(messages2[0], 'Success! Role Details Form saved.')
        self.assertEqual(res2.status_code, 200)


        data = {
            'title': '3',
            'position': '1',
            'programs': [],
            'current_page': CURRENT_PAGE2,
            'next': NEXT,
            'tab': TAB2
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(data, True), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User (firstname lastname, CWL: username) created.')
        self.assertEqual(res.status_code, 200)

        user = api.get_user(user_profile_form['username'], 'username')
        self.assertEqual(user.first_name, user_profile_form['first_name'])
        self.assertEqual(user.last_name, user_profile_form['last_name'])
        self.assertEqual(user.email, user_profile_form['email'])
        self.assertEqual(user.username, user_profile_form['username'])
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.profile.phone, user_profile_form['phone'])
        self.assertEqual(user.profile.office, user_profile_form['office'])
        self.assertEqual(user.profile.preferred_name, user_profile_form['preferred_name'])
        self.assertEqual(user.profile.roles.count(), len(user_profile_form['roles']))

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, user_profile_form['roles'])

        self.assertEqual(user.profile.title.id, int(data['title']))
        self.assertEqual(user.profile.position.id, int(data['position']))
        self.assertEqual(user.profile.programs.count(), len(data['programs']))

        programs = [ str(program.id) for program in user.profile.programs.all() ]
        self.assertEqual(programs, data['programs'])


    # prof form
    def test_create_prof_form_success1(self):
        print('- Test: create an user - prof form - success1 [4] [1]')
        self.login()

        TAB1 = 'basic_info'
        CURRENT_PAGE1 = '/admin/user/create/?next={0}&t={1}'.format(NEXT, TAB1)

        user_profile_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'preferred_name': 'preferred name',
            'is_superuser': 'on',
            'is_active': 'on',
            'roles': ['4'],
            'phone': 'phone',
            'office': 'office',
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1,
            'save': 'Save'
        }
        res1 = self.client.post(reverse('gp_admin:create_user'), data=urlencode(user_profile_form, True), content_type=ContentType, follow=True)
        messages1 = self.messages(res1)
        self.assertEqual(messages1[0], 'Success! Basic Information Form saved.')
        self.assertEqual(res1.status_code, 200)

        TAB2 = 'role_details'
        CURRENT_PAGE2 = '/admin/user/create/?next={0}&t={1}'.format(NEXT, TAB2)

        prof_form = {
            'title': '1',
            'position': '3',
            'programs': ['1'],
            'current_page': CURRENT_PAGE2,
            'next': NEXT,
            'tab': TAB2
        }

        res2 = self.client.post(reverse('gp_admin:create_user'), data=urlencode(prof_form, True), content_type=ContentType, follow=True)
        messages2 = self.messages(res2)
        self.assertEqual(messages2[0], 'Success! User (firstname lastname, CWL: username) created.')
        self.assertEqual(res2.status_code, 200)

        user = api.get_user(user_profile_form['username'], 'username')
        self.assertEqual(user.first_name, user_profile_form['first_name'])
        self.assertEqual(user.last_name, user_profile_form['last_name'])
        self.assertEqual(user.email, user_profile_form['email'])
        self.assertEqual(user.username, user_profile_form['username'])
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.profile.phone, user_profile_form['phone'])
        self.assertEqual(user.profile.office, user_profile_form['office'])
        self.assertEqual(user.profile.preferred_name, user_profile_form['preferred_name'])
        self.assertEqual(user.profile.roles.count(), len(user_profile_form['roles']))

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, user_profile_form['roles'])

        self.assertEqual(user.profile.title.id, int(prof_form['title']))
        self.assertEqual(user.profile.position.id, int(prof_form['position']))
        self.assertEqual(user.profile.programs.count(), len(prof_form['programs']))

        programs = [ str(program.id) for program in user.profile.programs.all() ]
        self.assertEqual(programs, prof_form['programs'])


    def test_create_prof_form_success2(self):
        print('- Test: create an user - prof form - success2 - [3,4] [1,2]')
        self.login()

        TAB1 = 'basic_info'
        CURRENT_PAGE1 = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB1)

        user_profile_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'preferred_name': 'preferred name',
            'is_superuser': 'on',
            'is_active': 'on',
            'roles': ['3','4'],
            'phone': 'phone',
            'office': 'office',
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1,
            'save': 'Save'
        }

        res1 = self.client.post(reverse('gp_admin:create_user'), data=urlencode(user_profile_form, True), content_type=ContentType, follow=True)
        messages1 = self.messages(res1)
        self.assertEqual(messages1[0], 'Success! Basic Information Form saved.')
        self.assertEqual(res1.status_code, 200)

        TAB2 = 'role_details'
        CURRENT_PAGE2 = '/admin/user/create/?next=/admin/users/all/?page=1&t={0}'.format(TAB2)
        prof_form = {
            'title': '1',
            'position': '3',
            'programs': ['1','2'],
            'current_page': CURRENT_PAGE2,
            'next': NEXT,
            'tab': TAB2
        }

        res2 = self.client.post(reverse('gp_admin:create_user'), data=urlencode(prof_form, True), content_type=ContentType, follow=True)
        messages2 = self.messages(res2)
        self.assertEqual(messages2[0], 'Success! User (firstname lastname, CWL: username) created.')
        self.assertEqual(res2.status_code, 200)

        user = api.get_user(user_profile_form['username'], 'username')
        self.assertEqual(user.first_name, user_profile_form['first_name'])
        self.assertEqual(user.last_name, user_profile_form['last_name'])
        self.assertEqual(user.email, user_profile_form['email'])
        self.assertEqual(user.username, user_profile_form['username'])
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.profile.phone, user_profile_form['phone'])
        self.assertEqual(user.profile.office, user_profile_form['office'])
        self.assertEqual(user.profile.preferred_name, user_profile_form['preferred_name'])
        self.assertEqual(user.profile.roles.count(), len(user_profile_form['roles']))

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, user_profile_form['roles'])

        self.assertEqual(user.profile.title.id, int(prof_form['title']))
        self.assertEqual(user.profile.position.id, int(prof_form['position']))
        self.assertEqual(user.profile.programs.count(), len(prof_form['programs']))

        programs = [ str(program.id) for program in user.profile.programs.all() ]
        self.assertEqual(programs, prof_form['programs'])'''


    def test_create_user_page(self):
        print('- Test: create a user - page')
        self.login()

        res = self.client.get(reverse('gp_admin:create_user') + '?next=' + NEXT + '&t=basic_info', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context['users']), 9)
        self.assertFalse(res.context['user_form'].is_bound)
        self.assertFalse(res.context['profile_form'].is_bound)
        self.assertFalse(res.context['prof_form'].is_bound)
        self.assertEqual(res.context['info'], {'btn_label': 'Create', 'href': '/admin/user/create/', 'type': 'create', 'path': 'users'})
        self.assertEqual(res.context['next'], NEXT)
        self.assertEqual(res.context['tab'], 'basic_info')
        self.assertEqual(res.context['tab_urls'], {'basic_info': '/admin/user/create/?next=/admin/users/all/?page=1&t=basic_info', 'role_details': '/admin/user/create/?next=/admin/users/all/?page=1&t=role_details'})


    # Edit user


    def test_edit_user_page(self):
        print('- Test: edit a user - page')
        self.login()

        res = self.client.get(reverse('gp_admin:edit_user', args=[USERS[1]]) + '?next=' + NEXT + '&t=basic_info', follow=True)
        self.assertEqual(res.status_code, 200)

        user = res.context['user']

        self.assertEqual(user.first_name, 'Guest1')
        self.assertEqual(user.last_name, 'Test')
        self.assertEqual(user.email, 'test.guest1@example.com')
        self.assertEqual(user.username, 'test.guest1')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_active)
        self.assertEqual(user.profile.preferred_name, 'Haha')
        self.assertEqual(user.profile.phone, '123-456-7890')
        self.assertEqual(user.profile.office, 'UBC')
        self.assertEqual(user.profile.roles.count(), 1)

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, ['5'])

        self.assertEqual(user.profile.title.id, 1)
        self.assertEqual(user.profile.position.id, 1)
        self.assertEqual(user.profile.programs.count(), 2)

        programs = [ str(program.id) for program in user.profile.programs.all() ]
        self.assertEqual(programs, ['1','2'])


    def test_no_changes_basic_info(self):
        print('- Test: edit a user - no changes - basic info')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/user/edit/?next=/admin/users/all/?page=1&t={0}'.format(TAB)
        
        u = api.get_user(USERS[0], 'username')

        user_profile_form = {
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'username': u.username,
            'is_superuser': u.is_superuser,
            'is_active': u.is_active,
            'preferred_name': u.profile.preferred_name,
            'roles': [ str(role.id) for role in u.profile.roles.all() ],
            'phone': u.profile.phone,
            'office': u.profile.office,
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id   
        }

        res = self.client.post(reverse('gp_admin:edit_user', args=[u.username]), data=urlencode(user_profile_form, True), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User ({0} {1}, CWL: {2}) updated.'.format(u.first_name, u.last_name, u.username))
        self.assertEqual(res.status_code, 200)


        user = api.get_user(u.username, 'username')

        self.assertEqual(user.first_name, u.first_name)
        self.assertEqual(user.last_name, u.last_name)
        self.assertEqual(user.email, u.email)
        self.assertEqual(user.username, u.username)
        self.assertFalse(u.is_superuser)
        self.assertTrue(u.is_active)
        self.assertEqual(user.profile.phone, u.profile.phone)
        self.assertEqual(user.profile.office, u.profile.office)
        self.assertEqual(user.profile.preferred_name, u.profile.preferred_name)
        self.assertEqual(user.profile.roles.count(), len(u.profile.roles.all()))

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, [ str(role.id) for role in u.profile.roles.all() ])

        self.assertEqual(str(user.profile.title.id), str(u.profile.title.id))
        self.assertEqual(str(user.profile.position.id), str(u.profile.position.id))
        self.assertEqual(user.profile.programs.count(), u.profile.programs.count())

        programs = [ str(program.id) for program in user.profile.programs.all() ]
        self.assertEqual(programs, [ str(program.id) for program in u.profile.programs.all() ])


    def test_no_changes_role_details(self):
        print('- Test: edit a user - no changes - role details')
        self.login()

        TAB = 'role_details'
        CURRENT_PAGE = '/admin/user/edit/?next=/admin/users/all/?page=1&t={0}'.format(TAB)

        u = api.get_user(USERS[0], 'username')

        prof_form = {
            'title': u.profile.title.id,
            'position': u.profile.position.id,
            'programs': [ str(program.id) for program in u.profile.programs.all() ],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id
        }

        res = self.client.post(reverse('gp_admin:edit_user', args=[u.username]), data=urlencode(prof_form, True), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User ({0} {1}, CWL: {2}) updated.'.format(u.first_name, u.last_name, u.username))
        self.assertEqual(res.status_code, 200)

        user = api.get_user(u.username, 'username')

        self.assertEqual(user.first_name, u.first_name)
        self.assertEqual(user.last_name, u.last_name)
        self.assertEqual(user.email, u.email)
        self.assertEqual(user.username, u.username)
        self.assertFalse(u.is_superuser)
        self.assertTrue(u.is_active)
        self.assertEqual(user.profile.phone, u.profile.phone)
        self.assertEqual(user.profile.office, u.profile.office)
        self.assertEqual(user.profile.preferred_name, u.profile.preferred_name)
        self.assertEqual(user.profile.roles.count(), len(u.profile.roles.all()))

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, [ str(role.id) for role in u.profile.roles.all() ])

        self.assertEqual(str(user.profile.title.id), str(u.profile.title.id))
        self.assertEqual(str(user.profile.position.id), str(u.profile.position.id))
        self.assertEqual(user.profile.programs.count(), u.profile.programs.count())

        programs = [ str(program.id) for program in user.profile.programs.all() ]
        self.assertEqual(programs, [ str(program.id) for program in u.profile.programs.all() ])


    def test_edit_user_profile_form_success1(self):
        print('- Test: edit a user - user profile form - success')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/user/edit/?next=/admin/users/all/?page=1&t={0}'.format(TAB)

        u = api.get_user(USERS[0], 'username')

        user_profile_form = {
            'first_name': 'newfirstname',
            'last_name': 'newlastname',
            'email': 'new.email@example.com',
            'username': 'new.username',
            'is_superuser': 'on',
            'is_active': '',
            'preferred_name': 'very good',
            'roles': ['3','4'],
            'phone': 'new phone',
            'office': 'new office',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id   
        }
        
        res = self.client.post(reverse('gp_admin:edit_user', args=[u.username]), data=urlencode(user_profile_form, True), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User (newfirstname newlastname, CWL: new.username) updated.')
        self.assertEqual(res.status_code, 200)

        user = api.get_user(user_profile_form['username'], 'username')

        self.assertEqual(user.first_name, user_profile_form['first_name'])
        self.assertEqual(user.last_name, user_profile_form['last_name'])
        self.assertEqual(user.email, user_profile_form['email'])
        self.assertEqual(user.username, user_profile_form['username'])
        self.assertTrue(user.is_superuser)
        self.assertFalse(user.is_active)
        self.assertEqual(user.profile.phone, user_profile_form['phone'])
        self.assertEqual(user.profile.office, user_profile_form['office'])
        self.assertEqual(user.profile.preferred_name, user_profile_form['preferred_name'])
        self.assertEqual(user.profile.roles.count(), len(user_profile_form['roles']))

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, user_profile_form['roles'])

        self.assertEqual(user.profile.title.id, u.profile.title.id)
        self.assertEqual(user.profile.position.id, u.profile.position.id)
        self.assertEqual(user.profile.programs.count(), u.profile.programs.count())

        programs = [ str(program.id) for program in user.profile.programs.all() ]
        self.assertEqual(programs, [ str(program.id) for program in u.profile.programs.all() ])


    def test_edit_user_profile_form_success2(self):
        print('- Test: edit a user - user profile form on different page - success')
        self.login()

        TAB1 = 'basic_info'
        CURRENT_PAGE1 = '/admin/user/edit/?next=/admin/users/all/?page=1&t={0}'.format(TAB1)

        u = api.get_user(USERS[0], 'username')

        TAB = 'role_details'
        CURRENT_PAGE = '/admin/user/edit/?next=/admin/users/all/?page=1&t={0}'.format(TAB)

        prof_form = {
            'title': u.profile.title.id,
            'position': u.profile.position.id,
            'programs': [ str(program.id) for program in u.profile.programs.all() ],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id
        }

        res = self.client.post(reverse('gp_admin:edit_user', args=[u.username]), data=urlencode(prof_form, True), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User (Prof User1, CWL: user1.prof) updated.')
        self.assertEqual(res.status_code, 200)

        user = api.get_user(u.username, 'username')

        self.assertEqual(user.first_name, u.first_name)
        self.assertEqual(user.last_name, u.last_name)
        self.assertEqual(user.email, u.email)
        self.assertEqual(user.username, u.username)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.profile.preferred_name, u.profile.preferred_name)
        self.assertEqual(user.profile.phone, u.profile.phone)
        self.assertEqual(user.profile.office, u.profile.office)
        self.assertEqual(user.profile.roles.count(), u.profile.roles.count())

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, [ str(role.id) for role in u.profile.roles.all() ])

        self.assertEqual(user.profile.title.id, u.profile.title.id)
        self.assertEqual(user.profile.position.id, u.profile.position.id)
        self.assertEqual(user.profile.programs.count(), u.profile.programs.count())

        programs = [ str(program.id) for program in user.profile.programs.all() ]
        self.assertEqual(programs, [ str(program.id) for program in u.profile.programs.all() ])


    '''def test_edit_user_profile_form_success3(self):
        print('- Test: edit a user - user profile form with different data - success')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/user/edit/?next=/admin/users/all/?page=1&t={0}'.format(TAB)
        
        u = api.get_user(USERS[0], 'username')

        user_profile_form = {
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'username': u.username,
            'is_superuser': u.is_superuser,
            'is_active': u.is_active,
            'preferred_name': u.profile.preferred_name,
            'roles': [ str(role.id) for role in u.profile.roles.all() ],
            'phone': u.profile.phone,
            'office': u.profile.office,
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id   
        }

        prof_form = {
            'title': str(u.profile.title.id),
            'position': str(u.profile.position.id),
            'programs': [ str(program.id) for program in u.profile.programs.all() ],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id
        }

        session = self.client.session
        session['save_user_profile_form'] = user_profile_form
        session['save_prof_form'] = prof_form
        session.save()

        data = {
            'first_name': 'newfirstname',
            'last_name': 'newlastname',
            'email': 'new.email@example.com',
            'username': 'new.username',
            'is_superuser': 'on',
            'is_active': '',
            'preferred_name': 'very good',
            'roles': ['3','4'],
            'phone': 'new phone',
            'office': 'new office',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id
        }

        res = self.client.post(reverse('gp_admin:edit_user', args=[u.username]), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User ({0} {1}, CWL: {2}) updated.'.format(data['first_name'], data['last_name'], data['username']))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, NEXT)
        self.assertRedirects(res, res.url)

        user = api.get_user(data['username'], 'username')

        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.username, data['username'])
        self.assertTrue(user.is_superuser)
        self.assertFalse(user.is_active)
        self.assertEqual(user.profile.phone, data['phone'])
        self.assertEqual(user.profile.office, data['office'])
        self.assertEqual(user.profile.preferred_name, data['preferred_name'])
        self.assertEqual(user.profile.roles.count(), len(data['roles']))

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, data['roles'])

        self.assertEqual(str(user.profile.title.id), prof_form['title'])
        self.assertEqual(str(user.profile.position.id), prof_form['position'])
        self.assertEqual(user.profile.programs.count(), len(prof_form['programs']))

        programs = [ str(program.id) for program in user.profile.programs.all() ]
        self.assertEqual(programs, prof_form['programs'])


    def test_edit_prof_form_success1(self):
        print('- Test: edit a user - prof form - success')
        self.login()

        TAB = 'role_details'
        CURRENT_PAGE = '/admin/user/edit/?next=/admin/users/all/?page=1&t={0}'.format(TAB)
        
        u = api.get_user(USERS[0], 'username')

        prof_form = {
            'title': '2',
            'position': '2',
            'programs': ['5'],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id
        }

        res = self.client.post(reverse('gp_admin:edit_user', args=[u.username]), data=urlencode(prof_form, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User ({0} {1}, CWL: {2}) updated.'.format(u.first_name, u.last_name, u.username))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, NEXT)
        self.assertRedirects(res, res.url)

        user = api.get_user(u.username, 'username')

        self.assertEqual(user.first_name, u.first_name)
        self.assertEqual(user.last_name, u.last_name)
        self.assertEqual(user.email, u.email)
        self.assertEqual(user.username, u.username)
        self.assertFalse(u.is_superuser)
        self.assertTrue(u.is_active)
        self.assertEqual(user.profile.phone, u.profile.phone)
        self.assertEqual(user.profile.office, u.profile.office)
        self.assertEqual(user.profile.preferred_name, u.profile.preferred_name)
        self.assertEqual(user.profile.roles.count(), len(u.profile.roles.all()))

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, [ str(role.id) for role in u.profile.roles.all() ])

        self.assertEqual(str(user.profile.title.id), prof_form['title'])
        self.assertEqual(str(user.profile.position.id), prof_form['position'])
        self.assertEqual(user.profile.programs.count(), len(prof_form['programs']))

        programs = [ str(program.id) for program in user.profile.programs.all() ]
        self.assertEqual(programs, prof_form['programs'])


    def test_edit_prof_form_success2(self):
        print('- Test: edit a user - prof form on different page - success')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/user/edit/?next=/admin/users/all/?page=1&t={0}'.format(TAB)
        
        u = api.get_user(USERS[0], 'username')

        prof_form = {
            'title': '2',
            'position': '2',
            'programs': ['5'],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id
        }

        session = self.client.session
        session['save_prof_form'] = prof_form
        session.save()

        user_profile_form = {
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'username': u.username,
            'is_superuser': u.is_superuser,
            'is_active': u.is_active,
            'preferred_name': u.profile.preferred_name,
            'roles': [ str(role.id) for role in u.profile.roles.all() ],
            'phone': u.profile.phone,
            'office': u.profile.office,
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id   
        }

        res = self.client.post(reverse('gp_admin:edit_user', args=[u.username]), data=urlencode(user_profile_form, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User ({0} {1}, CWL: {2}) updated.'.format(u.first_name, u.last_name, u.username))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, NEXT)
        self.assertRedirects(res, res.url)

        user = api.get_user(u.username, 'username')

        self.assertEqual(user.first_name, u.first_name)
        self.assertEqual(user.last_name, u.last_name)
        self.assertEqual(user.email, u.email)
        self.assertEqual(user.username, u.username)
        self.assertFalse(u.is_superuser)
        self.assertTrue(u.is_active)
        self.assertEqual(user.profile.phone, u.profile.phone)
        self.assertEqual(user.profile.office, u.profile.office)
        self.assertEqual(user.profile.preferred_name, u.profile.preferred_name)
        self.assertEqual(user.profile.roles.count(), len(u.profile.roles.all()))

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, [ str(role.id) for role in u.profile.roles.all() ])

        self.assertEqual(str(user.profile.title.id), prof_form['title'])
        self.assertEqual(str(user.profile.position.id), prof_form['position'])
        self.assertEqual(user.profile.programs.count(), len(prof_form['programs']))

        programs = [ str(program.id) for program in user.profile.programs.all() ]
        self.assertEqual(programs, prof_form['programs'])



    def test_edit_prof_form_success3(self):
        print('- Test: edit a user - prof form with different data - success')
        self.login()

        TAB = 'role_details'
        CURRENT_PAGE = '/admin/user/edit/?next=/admin/users/all/?page=1&t={0}'.format(TAB)
        
        u = api.get_user(USERS[0], 'username')

        user_profile_form = {
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'username': u.username,
            'is_superuser': u.is_superuser,
            'is_active': u.is_active,
            'preferred_name': u.profile.preferred_name,
            'roles': [ str(role.id) for role in u.profile.roles.all() ],
            'phone': u.profile.phone,
            'office': u.profile.office,
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id   
        }
        
        prof_form = {
            'title': str(u.profile.title.id),
            'position': str(u.profile.position.id),
            'programs': [ str(program.id) for program in u.profile.programs.all() ],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id
        }

        session = self.client.session
        session['save_user_profile_form'] = user_profile_form
        session['save_prof_form'] = prof_form
        session.save()

        data = {
            'title': '2',
            'position': '2',
            'programs': ['5'],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id
        }

        res = self.client.post(reverse('gp_admin:edit_user', args=[u.username]), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User ({0} {1}, CWL: {2}) updated.'.format(u.first_name, u.last_name, u.username))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, NEXT)
        self.assertRedirects(res, res.url)

        user = api.get_user(user_profile_form['username'], 'username')

        self.assertEqual(user.first_name, u.first_name)
        self.assertEqual(user.last_name, u.last_name)
        self.assertEqual(user.email, u.email)
        self.assertEqual(user.username, u.username)
        self.assertFalse(u.is_superuser)
        self.assertTrue(u.is_active)
        self.assertEqual(user.profile.phone, u.profile.phone)
        self.assertEqual(user.profile.office, u.profile.office)
        self.assertEqual(user.profile.preferred_name, u.profile.preferred_name)
        self.assertEqual(user.profile.roles.count(), len(u.profile.roles.all()))

        roles = [ str(role.id) for role in user.profile.roles.all() ]
        self.assertEqual(roles, [ str(role.id) for role in u.profile.roles.all() ])

        self.assertEqual(str(user.profile.title.id), data['title'])
        self.assertEqual(str(user.profile.position.id), data['position'])
        self.assertEqual(user.profile.programs.count(), len(data['programs']))

        programs = [ str(program.id) for program in user.profile.programs.all() ]
        self.assertEqual(programs, data['programs'])


    def test_edit_user_empty_title_success(self):
        print('- Test: edit a user - empty title - success')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/user/edit/?next=/admin/users/all/?page=1&t={0}'.format(TAB)
        
        u = api.get_user(USERS[1], 'username')

        user_profile_form = {
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'username': u.username,
            'is_superuser': u.is_superuser,
            'is_active': u.is_active,
            'preferred_name': u.profile.preferred_name,
            'roles': [ str(role.id) for role in u.profile.roles.all() ],
            'phone': u.profile.phone,
            'office': u.profile.office,
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id   
        }    
    
        res = self.client.post(reverse('gp_admin:edit_user', args=[u.username]), data=urlencode(user_profile_form, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User ({0} {1}, CWL: {2}) updated.'.format(u.first_name, u.last_name, u.username))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, NEXT)
        self.assertRedirects(res, res.url)
    

    def test_edit_user_empty_preferred_name_success(self):
        print('- Test: edit a user - empty preferred name - success')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/user/edit/?next=/admin/users/all/?page=1&t={0}'.format(TAB)
        
        u = api.get_user(USERS[1], 'username')

        user_profile_form = {
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'username': u.username,
            'is_superuser': u.is_superuser,
            'is_active': u.is_active,
            'preferred_name': u.profile.preferred_name,
            'roles': [ str(role.id) for role in u.profile.roles.all() ],
            'phone': u.profile.phone,
            'office': u.profile.office,
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB,
            'user': u.id   
        }    
    
        res = self.client.post(reverse('gp_admin:edit_user', args=[u.username]), data=urlencode(user_profile_form, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User ({0} {1}, CWL: {2}) updated.'.format(u.first_name, u.last_name, u.username))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, NEXT)
        self.assertRedirects(res, res.url)'''
    