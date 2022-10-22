from django.conf import settings
from django.test import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse
from urllib.parse import urlencode
import datetime

from gp_admin import api

from gp_admin.tests.users import LOGIN_URL, ContentType, DATA, USERS, USER_IDS, PASSWORD


NEXT = '/admin/students/?page=1'

class StudentTest(TestCase):
    fixtures = DATA

    @classmethod
    def setUpTestData(cls):
        #print('\Student testing has started ==>')
        cls.user = api.get_user(USERS[0], 'username')

    def login(self, username=None, password=None):
        if username and password:
            self.client.post(LOGIN_URL, data={'username': username, 'password': password})
        else:
            self.client.post(LOGIN_URL, data={'username': self.user.username, 'password': PASSWORD})

    def messages(self, res):
        return [m.message for m in get_messages(res.wsgi_request)]
    

    '''def test_missing_required_fields_first_name(self):
        print('- Test: create a student - missing required fields - first name')
        self.login()

        TAB = 'basic_student'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/?page=1&t={0}'.format(TAB)
        
        data = {
            'first_name': '',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': 'email@example.com',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. FIRST NAME: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)

    def test_missing_required_fields_last_name(self):
        print('- Test: create a student - missing required fields - last name')
        self.login()

        TAB = 'basic_student'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/?page=1&t={0}'.format(TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': '',
            'student_number': '90000222',
            'email': 'email@example.com',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. LAST NAME: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)

    def test_missing_required_fields_student_number(self):
        print('- Test: create a student - missing required fields - student number')
        self.login()

        TAB = 'basic_student'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/?page=1&t={0}'.format(TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '',
            'email': 'email@example.com',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. STUDENT NUMBER: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)

    def test_missing_required_fields_email(self):
        print('- Test: create a student - missing required fields - email')
        self.login()

        TAB = 'basic_student'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/?page=1&t={0}'.format(TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': '',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. EMAIL: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)'''


    '''def test_wrong_email(self):
        print('- Test: create a student - wrong email')
        self.login()

        TAB = 'basic_student'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/?page=1&t={0}'.format(TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': 'email',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. EMAIL: Enter a valid email address.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)


    def test_loa_months_min_failure(self):
        print('- Test: create a student - loa months - min failure')
        self.login()

        TAB = 'basic_student'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/?page=1&t={0}'.format(TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': 'email@example.com',
            'loa_months': -1,
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. LOA MONTHS: Ensure this value is greater than or equal to 0.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)



    def test_loa_months_max_failure(self):
        print('- Test: create a student - loa months - max failure')
        self.login()

        TAB = 'basic_student'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/?page=1&t={0}'.format(TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': 'email@example.com',
            'loa_months': 201,
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data, True), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. LOA MONTHS: Ensure this value is less than or equal to 200.')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, res.url)'''
    

    # Basic Student

    '''def test_basic_student_form_only(self):
        print('- Test: create an student - basic_student form only')
        self.login()

        TAB = 'basic_student'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB)

        basic_student_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'student_number': '90000888',
            'date_of_birth': '1990-01-01', 
            'phone': '123-456-7890', 
            'sin': '987-654-321', 
            'loa_months': '5', 
            'loa_details': 'loa details', 
            'policy_85': 'on', 
            'note': '<p>note</p>',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(basic_student_form, True), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! Student (firstname lastname, Student #: 90000888) created.')
        self.assertEqual(res.status_code, 200)

        stud = api.get_student(basic_student_form['student_number'])
        self.assertEqual(stud.first_name, basic_student_form['first_name'])
        self.assertEqual(stud.last_name, basic_student_form['last_name'])
        self.assertEqual(stud.student_number, basic_student_form['student_number'])
        self.assertEqual(stud.email, basic_student_form['email'])
        self.assertEqual(stud.date_of_birth, datetime.date(1990, 1, 1))
        self.assertEqual(stud.phone, basic_student_form['phone'])
        self.assertEqual(stud.sin, basic_student_form['sin'])
        self.assertEqual(stud.loa_months, int(basic_student_form['loa_months']))
        self.assertEqual(stud.loa_details, basic_student_form['loa_details'])
        self.assertTrue(stud.policy_85)
        self.assertEqual(stud.note, basic_student_form['note'])'''

    def test_basic_student_form_after_saved(self):
        print('- Test: create an student - basic_student form after saved')
        self.login()

        TAB = 'basic_student'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB)

        temp = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'student_number': '90000888',
            'date_of_birth': '1990-01-01',
            'phone': '123-456-7890', 
            'sin': '987-654-321', 
            'loa_months': '5', 
            'loa_details': 'loa details', 
            'policy_85': 'on', 
            'note': '<p>note</p>',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB,
            'save': 'Save'
        }
        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(temp), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! Basic Student Form saved.')
        self.assertEqual(res.status_code, 200)
        



    '''def test_current_school_info_form_only(self):
        print('- Test: create a student - current school info form only')
        self.login()

        TAB = 'current_school_info'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB)

        current_shcool_info_form = {
            'status': '1', 
            'start_date': '2021-01-01', 
            'completion_date': '2022-01-01', 
            'graduation_date': '2022-05-01', 
            'comprehensive_exam_date': '2021-12-12',
            'thesis_title': 'title', 
            'funding_sources': 'school', 
            'total_funding_awarded': '2', 
            'taships': 'taships', 
            'current_role': 'researcher',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(current_shcool_info_form, True), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. FIRST NAME: This field is required. LAST NAME: This field is required. STUDENT NUMBER: This field is required. EMAIL: This field is required.')'''


    '''def test_current_school_info_form_success(self):
        print('- Test: create a student - current school info form success')
        self.login()

        TAB = 'current_school_info'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB)

        basic_student_form = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@example.com',
            'student_number': '90000888',
            'date_of_birth': '1990-01-01', 
            'phone': '123-456-7890', 
            'sin': '987-654-321', 
            'loa_months': '5', 
            'loa_details': 'loa details', 
            'policy_85': 'on', 
            'note': '<p>note</p>',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB,
            'save': 'Save'
        }

        #res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(basic_student_form), content_type=ContentType, follow=True)
        #messages = self.messages(res)
        #print(messages)

        current_shcool_info_form = {
            'status': '1', 
            'start_date': '2021-01-01', 
            'completion_date': '2022-01-01', 
            'graduation_date': '2022-05-01', 
            'comprehensive_exam_date': '2021-12-12',
            'thesis_title': 'title', 
            'funding_sources': 'school', 
            'total_funding_awarded': '2', 
            'taships': 'taships', 
            'current_role': 'researcher',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        #res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(current_shcool_info_form, True), content_type=ContentType, follow=True)
        #messages = self.messages(res)
        #print(messages)
        #self.assertEqual(res.status_code, 200)
        #self.assertEqual(messages[0], 'An error occurred. Form is invalid. FIRST NAME: This field is required. LAST NAME: This field is required. STUDENT NUMBER: This field is required. EMAIL: This field is required.')'''



    '''def test_previous_school_info_form_only(self):
        print('- Test: create a student - previous school info form only')
        self.login()

        TAB = 'previous_school_info'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB)

        previous_shcool_info_form = {
            'previous_institution_1': 'previous_institution_1', 
            'degree_1': 'degree_1', 
            'gpa_1': '1.1', 
            'previous_institution_2': 'previous_institution_2', 
            'degree_2': 'degree_2', 
            'gpa_2': '2.2', 
            'previous_institution_3': 'previous_institution_3', 
            'degree_3': 'degree_3', 
            'gpa_3': '3.3',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'current_tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(previous_shcool_info_form, True), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. FIRST NAME: This field is required. LAST NAME: This field is required. STUDENT NUMBER: This field is required. EMAIL: This field is required.')'''


'''def test_cancel_student(self):
        print('- Test: cancel a student')
        self.login()

        TAB = 'basic_student'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB)

        session = self.client.session
        session['save_student_form'] = {
            'basic_student': {
                'first_name': 'firstname',
                'last_name': 'lastname',
                'student_number': '90000222',
                'email': 'email@example.com'
            },
            'current_school_info': {
                'status': '1'
            },
            'previous_school_info': {
                'previous_institution_1': 'institution'
            }
        }
        
        session.save()

        res = self.client.get( reverse('gp_admin:cancel_student') + '?next=' + NEXT, follow=True )
        print(res)
        #self.assertEqual(res.status_code, 200)
        #self.assertRedirects(res, res.url)
        #self.assertEqual(res.url, NEXT)
        
        print(session.get('save_student_form'))'''

