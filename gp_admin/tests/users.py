from django.conf import settings
from django.test import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse
from urllib.parse import urlencode

from gp_admin import api


LOGIN_URL = '/accounts/local_login/'
ContentType='application/x-www-form-urlencoded'

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
    'gp_admin/fixtures/users.json',
]

USERS = [ 'haha.superadmin']
USER_IDS = [1]

PASSWORD = 'password'


CURRENT_PAGE = '/admin/user/create/?next=/admin/users/all/&t=User'
NEXT = '/admin/users/all/?page=1'

class UserTest(TestCase):
    fixtures = DATA

    @classmethod
    def setUpTestData(cls):
        print('\nSession testing has started ==>')
        cls.user = api.get_user(USERS[0], 'username')

    def login(self, username=None, password=None):
        if username and password:
            self.client.post(LOGIN_URL, data={'username': username, 'password': password})
        else:
            self.client.post(LOGIN_URL, data={'username': self.user.username, 'password': PASSWORD})

    def messages(self, res):
        return [m.message for m in get_messages(res.wsgi_request)]
    
    def test_get_users(self):
        print('- Test: get users')

        self.login()
        res = self.client.get( reverse('gp_admin:get_users') )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context['users']), 9)
        self.assertEqual(res.context['total_users'], 9)

    def test_create_user_missing_required_fields_firstname(self):
        print('- Test: create an user - missing required fields - first name')
        self.login()

        data = {
            'first_name': '',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'preferred_name': 'preferred name',
            'is_superuser': 'on',
            'is_active': 'on',
            'roles': ['1'],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': 'User'
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res) 
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. FIRST NAME: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)

    def test_create_user_missing_required_fields_lastname(self):
        print('- Test: create an user - missing required fields - last name')
        self.login()

        data = {
            'first_name': 'firstname',
            'last_name': '',
            'email': 'email@example.com',
            'username': 'username',
            'preferred_name': 'preferred name',
            'is_superuser': 'on',
            'is_active': 'on',
            'roles': ['1'],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': 'User'
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res) 
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. LAST NAME: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)

    def test_create_user_missing_required_fields_email(self):
        print('- Test: create an user - missing required fields - email')
        self.login()

        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': '',
            'username': 'username',
            'preferred_name': 'preferred name',
            'is_superuser': 'on',
            'is_active': 'on',
            'roles': ['1'],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': 'User'
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res) 
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. EMAIL: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)

    def test_create_user_missing_required_fields_username(self):
        print('- Test: create an user - missing required fields - username')
        self.login()

        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': '',
            'preferred_name': 'preferred name',
            'is_superuser': 'on',
            'is_active': 'on',
            'roles': ['1'],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': 'User'
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res) 
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. USERNAME: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)

    def test_create_user_missing_required_fields_roles(self):
        print('- Test: create an user - missing required fields - roles')
        self.login()

        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'preferred_name': 'preferred name',
            'is_superuser': 'on',
            'is_active': 'on',
            'roles': [],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': 'User'
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res) 
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. ROLES: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)

    def test_create_user_user_profile_form_only(self):
        print('- Test: create an user - user profile form only')
        self.login()

        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'preferred_name': 'preferred name',
            'is_superuser': '',
            'is_active': 'on',
            'roles': ['4'],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': 'User'
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res) 
        self.assertEqual(messages[0], 'Success! User (firstname lastname, CWL: username) created.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)

        u = api.get_user(data['username'], 'username')
        self.assertEqual(u.first_name, data['first_name'])
        self.assertEqual(u.last_name, data['last_name'])
        self.assertEqual(u.email, data['email'])
        self.assertEqual(u.username, data['username'])
        self.assertFalse(u.is_superuser)
        self.assertTrue(u.is_active)
        self.assertEqual(u.profile.preferred_name, data['preferred_name'])

        roles = [ role.name for role in u.profile.roles.all() ]
        self.assertEqual(roles, ['Supervisor'])


    def test_create_prof_form_success1(self):
        print('- Test: create an user - prof form - success [1] [1]')
        self.login()

        TAB = 'Professor'

        user_profile_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'preferred_name': 'preferred name',
            'is_superuser': 'on',
            'is_active': 'on',
            'roles': ['4'],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        session = self.client.session
        session['save_user_profile_form'] = user_profile_form
        session.save()

        prof_form = {
            'title': '1',
            'position': '',
            'programs': ['1'],
            'phone': 'phone',
            'fax': 'fax',
            'office': 'office',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(prof_form, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User (firstname lastname, CWL: username) created.')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, NEXT)
        self.assertRedirects(res, res.url)

        u = api.get_user(user_profile_form['username'], 'username')
        self.assertEqual(u.first_name, user_profile_form['first_name'])
        self.assertEqual(u.last_name, user_profile_form['last_name'])
        self.assertEqual(u.email, user_profile_form['email'])
        self.assertEqual(u.username, user_profile_form['username'])
        self.assertTrue(u.is_superuser)
        self.assertTrue(u.is_active)
        self.assertEqual(u.profile.preferred_name, data['preferred_name'])
        self.assertEqual(u.profile.title, '')

        roles = [ role.name for role in u.profile.roles.all() ]
        self.assertEqual(roles, ['Supervisor'])


    def test_create_prof_form_success2(self):
        print('- Test: create an user - prof form - success [3,4] [1]')
        self.login()

        TAB = 'Professor'

        user_profile_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'preferred_name': 'preferred name',
            'is_superuser': 'on',
            'is_active': 'on',
            'roles': ['3', '4'],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        session = self.client.session
        session['save_user_profile_form'] = user_profile_form
        session.save()

        prof_form = {
            'title': '1',
            'position': '',
            'programs': ['1'],
            'phone': 'phone',
            'fax': 'fax',
            'office': 'office',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(prof_form, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User (firstname lastname, CWL: username) created.')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, NEXT)
        self.assertRedirects(res, res.url)



    def test_create_user_profile_form_success1(self):
        print('- Test: create an user - user profile form - success [3,4] [1,2]')
        self.login()

        TAB = 'User'

        user_profile_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'username': 'username',
            'preferred_name': 'preferred name',
            'is_superuser': 'on',
            'is_active': 'on',
            'roles': ['3', '4'],
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        prof_form = {
            'title': '1',
            'position': '',
            'programs': ['1','2'],
            'phone': 'phone',
            'fax': 'fax',
            'office': 'office',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        session = self.client.session
        session['save_prof_form'] = prof_form
        session.save()

        res = self.client.post(reverse('gp_admin:create_user'), data=urlencode(prof_form, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! User (firstname lastname, CWL: username) created.')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, NEXT)
        self.assertRedirects(res, res.url)


