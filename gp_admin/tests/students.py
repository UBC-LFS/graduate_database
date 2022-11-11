from django.conf import settings
from django.test import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse
from urllib.parse import urlencode
import datetime

from gp_admin import api

from gp_admin.tests.users import LOGIN_URL, ContentType, DATA, USERS, USER_IDS, PASSWORD

STUDENTS = ['90000001']

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
    


    # Create Student

    def test_create_student_page(self):
        print('- Test: create a student - page')
        self.login()

        res = self.client.get(reverse('gp_admin:create_student') + '?next=' + NEXT + '&t=basic_info', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context['students']), 5)
        self.assertFalse(res.context['form'].is_bound)
        self.assertEqual(res.context['info'], {'btn_label': 'Create', 'type': 'create', 'path': 'students'})
        self.assertEqual(res.context['next'], NEXT)
        self.assertEqual(res.context['tab'], 'basic_info')
        self.assertEqual(res.context['tab_urls'], {'basic_info': '/admin/student/create/?next=/admin/students/?page=1&t=basic_info', 'additional_info': '/admin/student/create/?next=/admin/students/?page=1&t=additional_info', 'previous_school_info': '/admin/student/create/?next=/admin/students/?page=1&t=previous_school_info'})


    def test_create_student_missing_required_fields_first_name(self):
        print('- Test: create a student - missing required fields - first name')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/?page=1&t={0}'.format(TAB)
        
        data = {
            'first_name': '',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': 'email@example.com',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. FIRST NAME: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, CURRENT_PAGE)
        self.assertRedirects(res, res.url)


    def test_create_student_missing_required_fields_last_name(self):
        print('- Test: create a student - missing required fields - last name')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/?page=1&t={0}'.format(TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': '',
            'student_number': '90000222',
            'email': 'email@example.com',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. LAST NAME: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, CURRENT_PAGE)
        self.assertRedirects(res, res.url)


    def test_create_student_missing_required_fields_student_number(self):
        print('- Test: create a student - missing required fields - student number')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/?page=1&t={0}'.format(TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '',
            'email': 'email@example.com',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. STUDENT NUMBER: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, CURRENT_PAGE)
        self.assertRedirects(res, res.url)

    def test_create_student_missing_required_fields_email(self):
        print('- Test: create a student - missing required fields - email')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/?page=1&t={0}'.format(TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': '',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. EMAIL: This field is required.')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, CURRENT_PAGE)
        self.assertRedirects(res, res.url)


    def test_create_student_wrong_email(self):
        print('- Test: create a student - wrong email')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/?page=1&t={0}'.format(TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': 'email',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. EMAIL: Enter a valid email address.')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, CURRENT_PAGE)
        self.assertRedirects(res, res.url)


    def test_create_student_loa_months_min_failure(self):
        print('- Test: create a student - loa months - min failure')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/?page=1&t={0}'.format(TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': 'email@example.com',
            'loa_months': -1,
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. LOA MONTHS: Ensure this value is greater than or equal to 0.')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, CURRENT_PAGE)
        self.assertRedirects(res, res.url)


    def test_create_student_loa_months_max_failure(self):
        print('- Test: create a student - loa months - max failure')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/?page=1&t={0}'.format(TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': 'email@example.com',
            'loa_months': 201,
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. LOA MONTHS: Ensure this value is less than or equal to 200.')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, CURRENT_PAGE)
        self.assertRedirects(res, res.url)
    

    # Basic Information

    def test_create_student_tab_error(self):
        print('- Test: craete a student - tab error')
        self.login()

        TAB = 'basic_infoa'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB)

        data = {
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
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. No valid tab.')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, CURRENT_PAGE)
        self.assertRedirects(res, res.url)


    def test_create_student_basic_info_only(self):
        print('- Test: create an student - basic info only')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB)

        data = {
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
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! Student (firstname lastname, Student #: 90000888) created.')
        self.assertEqual(res.status_code, 200)

        stud = api.get_student_by_sn(data['student_number'])
        self.assertEqual(stud.first_name, data['first_name'])
        self.assertEqual(stud.last_name, data['last_name'])
        self.assertEqual(stud.student_number, data['student_number'])
        self.assertEqual(stud.email, data['email'])
        self.assertEqual(stud.date_of_birth, datetime.date(1990, 1, 1))
        self.assertEqual(stud.phone, data['phone'])
        self.assertEqual(stud.sin, data['sin'])
        self.assertEqual(stud.loa_months, int(data['loa_months']))
        self.assertEqual(stud.loa_details, data['loa_details'])
        self.assertTrue(stud.policy_85)
        self.assertEqual(stud.note, data['note'])


    def test_create_student_basic_info_after_saved(self):
        print('- Test: create an student - basic info form after saved')
        self.login()

        TAB1 = 'basic_info'
        CURRENT_PAGE1 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB1)

        data1 = {
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
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1,
            'save': 'Save'
        }
        res1 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data1), content_type=ContentType, follow=True)
        messages1 = self.messages(res1)
        self.assertEqual(messages1[0], 'Success! Basic Information Form saved.')
        self.assertEqual(res1.status_code, 200)

        TAB2 = 'additional_info'
        CURRENT_PAGE2 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB2)
        data2 = {
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
            'current_page': CURRENT_PAGE2,
            'next': NEXT,
            'tab': TAB2,
            'save': 'Save'
        }
        res2 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data2), content_type=ContentType, follow=True)
        messages2 = self.messages(res2)
        self.assertEqual(messages2[0], 'Success! Additional Information Form saved.')
        self.assertEqual(res2.status_code, 200)

        data3 = {
            'first_name': 'firstname1',
            'last_name': 'lastname1',
            'email': 'email1@example.com',
            'student_number': '90000881',
            'date_of_birth': '1990-01-02',
            'phone': '123-456-7891', 
            'sin': '987-654-322', 
            'loa_months': '3', 
            'loa_details': 'loa details1', 
            'policy_85': '', 
            'note': '<p>note1</p>',
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1
        }
        res3 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data3), content_type=ContentType, follow=True)
        messages3 = self.messages(res3)
        self.assertEqual(messages3[0], 'Success! Student (firstname1 lastname1, Student #: 90000881) created.')
        self.assertEqual(res3.status_code, 200)
        
        stud = api.get_student_by_sn(data3['student_number'])
        self.assertEqual(stud.first_name, data3['first_name'])
        self.assertEqual(stud.last_name, data3['last_name'])
        self.assertEqual(stud.student_number, data3['student_number'])
        self.assertEqual(stud.email, data3['email'])
        self.assertEqual(stud.date_of_birth, datetime.date(1990, 1, 2))
        self.assertEqual(stud.phone, data3['phone'])
        self.assertEqual(stud.sin, data3['sin'])
        self.assertEqual(stud.loa_months, int(data3['loa_months']))
        self.assertEqual(stud.loa_details, data3['loa_details'])
        self.assertFalse(stud.policy_85)
        self.assertEqual(stud.note, data3['note'])

        self.assertEqual(stud.status.id, int(data2['status']))
        self.assertEqual(stud.start_date, datetime.date(2021, 1, 1))
        self.assertEqual(stud.completion_date, datetime.date(2022, 1, 1))
        self.assertEqual(stud.graduation_date, datetime.date(2022, 5, 1))
        self.assertEqual(stud.comprehensive_exam_date, datetime.date(2021, 12, 12))
        self.assertEqual(stud.thesis_title, data2['thesis_title'])
        self.assertEqual(stud.funding_sources, data2['funding_sources'])
        self.assertEqual(stud.total_funding_awarded, data2['total_funding_awarded'])
        self.assertEqual(stud.taships, data2['taships'])
        self.assertEqual(stud.current_role, data2['current_role'])


    # Additional Informaion

    def test_create_student_additional_info_only(self):
        print('- Test: create a student - additional info only')
        self.login()

        TAB = 'additional_info'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB)

        data = {
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
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. FIRST NAME: This field is required. LAST NAME: This field is required. STUDENT NUMBER: This field is required. EMAIL: This field is required.')


    def test_create_student_additional_info_form_success(self):
        print('- Test: create a student - additional info - success')
        self.login()

        TAB1 = 'basic_info'
        CURRENT_PAGE1 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB1)

        data1 = {
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
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1,
            'save': 'Save'
        }

        res1 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data1), content_type=ContentType, follow=True)
        messages1 = self.messages(res1)
        self.assertEqual(messages1[0], 'Success! Basic Information Form saved.')
        self.assertEqual(res1.status_code, 200)

        TAB2 = 'additional_info'
        CURRENT_PAGE2 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB2)

        data2 = {
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
            'current_page': CURRENT_PAGE2,
            'next': NEXT,
            'tab': TAB2
        }

        res2 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data2), content_type=ContentType, follow=True)
        messages2 = self.messages(res2)
        self.assertEqual(messages2[0], 'Success! Student (firstname lastname, Student #: 90000888) created.')
        self.assertEqual(res2.status_code, 200)
        
        stud = api.get_student_by_sn(data1['student_number'])
        self.assertEqual(stud.first_name, data1['first_name'])
        self.assertEqual(stud.last_name, data1['last_name'])
        self.assertEqual(stud.student_number, data1['student_number'])
        self.assertEqual(stud.email, data1['email'])
        self.assertEqual(stud.date_of_birth, datetime.date(1990, 1, 1))
        self.assertEqual(stud.phone, data1['phone'])
        self.assertEqual(stud.sin, data1['sin'])
        self.assertEqual(stud.loa_months, int(data1['loa_months']))
        self.assertEqual(stud.loa_details, data1['loa_details'])
        self.assertTrue(stud.policy_85)
        self.assertEqual(stud.note, data1['note'])

        self.assertEqual(stud.status.id, int(data2['status']))
        self.assertEqual(stud.start_date, datetime.date(2021, 1, 1))
        self.assertEqual(stud.completion_date, datetime.date(2022, 1, 1))
        self.assertEqual(stud.graduation_date, datetime.date(2022, 5, 1))
        self.assertEqual(stud.comprehensive_exam_date, datetime.date(2021, 12, 12))
        self.assertEqual(stud.thesis_title, data2['thesis_title'])
        self.assertEqual(stud.funding_sources, data2['funding_sources'])
        self.assertEqual(stud.total_funding_awarded, data2['total_funding_awarded'])
        self.assertEqual(stud.taships, data2['taships'])
        self.assertEqual(stud.current_role, data2['current_role'])


    def test_create_student_previous_school_info_only(self):
        print('- Test: create a student - previous school info only')
        self.login()

        TAB = 'previous_school_info'
        CURRENT_PAGE = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB)

        data = {
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
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. FIRST NAME: This field is required. LAST NAME: This field is required. STUDENT NUMBER: This field is required. EMAIL: This field is required.')


    def test_create_student_previous_school_info_success(self):
        print('- Test: create a student - previous school info - success')
        self.login()

        TAB1 = 'basic_info'
        CURRENT_PAGE1 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB1)

        data1 = {
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
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1,
            'save': 'Save'
        }

        res1 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data1), content_type=ContentType, follow=True)
        messages1 = self.messages(res1)
        self.assertEqual(messages1[0], 'Success! Basic Information Form saved.')
        self.assertEqual(res1.status_code, 200)

        TAB2 = 'previous_school_info'
        CURRENT_PAGE2 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB2)

        data2 = {
            'previous_institution_1': 'previous_institution_1', 
            'degree_1': 'degree_1', 
            'gpa_1': '1.1', 
            'previous_institution_2': 'previous_institution_2', 
            'degree_2': 'degree_2', 
            'gpa_2': '2.2', 
            'previous_institution_3': 'previous_institution_3', 
            'degree_3': 'degree_3', 
            'gpa_3': '3.3',
            'current_page': CURRENT_PAGE2,
            'next': NEXT,
            'tab': TAB2
        }

        res2 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data2), content_type=ContentType, follow=True)
        messages2 = self.messages(res2)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(messages2[0], 'Success! Student (firstname lastname, Student #: 90000888) created.')

        stud = api.get_student_by_sn(data1['student_number'])
        self.assertEqual(stud.first_name, data1['first_name'])
        self.assertEqual(stud.last_name, data1['last_name'])
        self.assertEqual(stud.student_number, data1['student_number'])
        self.assertEqual(stud.email, data1['email'])
        self.assertEqual(stud.date_of_birth, datetime.date(1990, 1, 1))
        self.assertEqual(stud.phone, data1['phone'])
        self.assertEqual(stud.sin, data1['sin'])
        self.assertEqual(stud.loa_months, int(data1['loa_months']))
        self.assertEqual(stud.loa_details, data1['loa_details'])
        self.assertTrue(stud.policy_85)
        self.assertEqual(stud.note, data1['note'])

        self.assertEqual(stud.previous_institution_1, data2['previous_institution_1'])
        self.assertEqual(stud.degree_1, data2['degree_1'])
        self.assertEqual(stud.gpa_1, data2['gpa_1'])
        self.assertEqual(stud.previous_institution_2, data2['previous_institution_2'])
        self.assertEqual(stud.degree_2, data2['degree_2'])
        self.assertEqual(stud.gpa_2, data2['gpa_2'])
        self.assertEqual(stud.previous_institution_3, data2['previous_institution_3'])
        self.assertEqual(stud.degree_3, data2['degree_3'])
        self.assertEqual(stud.gpa_3, data2['gpa_3'])
        

    def test_create_student_three_tabs_basic_info_success(self):
        print('- Test: create a student - three tabs - basic info - success')
        self.login()

        TAB1 = 'basic_info'
        CURRENT_PAGE1 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB1)

        data1 = {
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
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1,
            'save': 'Save'
        }

        res1 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data1), content_type=ContentType, follow=True)
        messages1 = self.messages(res1)
        self.assertEqual(messages1[0], 'Success! Basic Information Form saved.')
        self.assertEqual(res1.status_code, 200)


        TAB2 = 'additional_info'
        CURRENT_PAGE2 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB2)

        data2 = {
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
            'current_page': CURRENT_PAGE2,
            'next': NEXT,
            'tab': TAB2,
            'save': 'Save'
        }
        res2 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data2), content_type=ContentType, follow=True)
        messages2 = self.messages(res2)
        self.assertEqual(messages2[0], 'Success! Additional Information Form saved.')
        self.assertEqual(res2.status_code, 200)


        TAB3 = 'previous_school_info'
        CURRENT_PAGE3 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB3)

        data3 = {
            'previous_institution_1': 'previous_institution_1', 
            'degree_1': 'degree_1', 
            'gpa_1': '1.1', 
            'previous_institution_2': 'previous_institution_2', 
            'degree_2': 'degree_2', 
            'gpa_2': '2.2', 
            'previous_institution_3': 'previous_institution_3', 
            'degree_3': 'degree_3', 
            'gpa_3': '3.3',
            'current_page': CURRENT_PAGE3,
            'next': NEXT,
            'tab': TAB3,
            'save': 'Save'
        }

        res3 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data3), content_type=ContentType, follow=True)
        messages3 = self.messages(res3)
        self.assertEqual(res3.status_code, 200)
        self.assertEqual(messages3[0], 'Success! Previous School Information Form saved.')

        data4 = {
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
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1
        }

        res4 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data4), content_type=ContentType, follow=True)
        messages4 = self.messages(res4)
        self.assertEqual(messages4[0], 'Success! Student (firstname lastname, Student #: 90000888) created.')
        self.assertEqual(res4.status_code, 200)

        stud = api.get_student_by_sn(data4['student_number'])
        self.assertEqual(stud.first_name, data4['first_name'])
        self.assertEqual(stud.last_name, data4['last_name'])
        self.assertEqual(stud.student_number, data4['student_number'])
        self.assertEqual(stud.email, data4['email'])
        self.assertEqual(stud.date_of_birth, datetime.date(1990, 1, 1))
        self.assertEqual(stud.phone, data4['phone'])
        self.assertEqual(stud.sin, data4['sin'])
        self.assertEqual(stud.loa_months, int(data4['loa_months']))
        self.assertEqual(stud.loa_details, data4['loa_details'])
        self.assertTrue(stud.policy_85)
        self.assertEqual(stud.note, data4['note'])
        
        self.assertEqual(stud.status.id, int(data2['status']))
        self.assertEqual(stud.start_date, datetime.date(2021, 1, 1))
        self.assertEqual(stud.completion_date, datetime.date(2022, 1, 1))
        self.assertEqual(stud.graduation_date, datetime.date(2022, 5, 1))
        self.assertEqual(stud.comprehensive_exam_date, datetime.date(2021, 12, 12))
        self.assertEqual(stud.thesis_title, data2['thesis_title'])
        self.assertEqual(stud.funding_sources, data2['funding_sources'])
        self.assertEqual(stud.total_funding_awarded, data2['total_funding_awarded'])
        self.assertEqual(stud.taships, data2['taships'])
        self.assertEqual(stud.current_role, data2['current_role'])

        self.assertEqual(stud.previous_institution_1, data3['previous_institution_1'])
        self.assertEqual(stud.degree_1, data3['degree_1'])
        self.assertEqual(stud.gpa_1, data3['gpa_1'])
        self.assertEqual(stud.previous_institution_2, data3['previous_institution_2'])
        self.assertEqual(stud.degree_2, data3['degree_2'])
        self.assertEqual(stud.gpa_2, data3['gpa_2'])
        self.assertEqual(stud.previous_institution_3, data3['previous_institution_3'])
        self.assertEqual(stud.degree_3, data3['degree_3'])
        self.assertEqual(stud.gpa_3, data3['gpa_3'])
        


    def test_three_tabs_additional_info_success(self):
        print('- Test: create a student - three tabs - additional info - success')
        self.login()

        TAB1 = 'basic_info'
        CURRENT_PAGE1 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB1)

        data1 = {
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
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1,
            'save': 'Save'
        }

        res1 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data1), content_type=ContentType, follow=True)
        messages1 = self.messages(res1)
        self.assertEqual(messages1[0], 'Success! Basic Information Form saved.')
        self.assertEqual(res1.status_code, 200)


        TAB2 = 'additional_info'
        CURRENT_PAGE2 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB2)

        data2 = {
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
            'current_page': CURRENT_PAGE2,
            'next': NEXT,
            'tab': TAB2,
            'save': 'Save'
        }
        res2 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data2), content_type=ContentType, follow=True)
        messages2 = self.messages(res2)
        self.assertEqual(messages2[0], 'Success! Additional Information Form saved.')
        self.assertEqual(res2.status_code, 200)


        TAB3 = 'previous_school_info'
        CURRENT_PAGE3 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB3)

        data3 = {
            'previous_institution_1': 'previous_institution_1', 
            'degree_1': 'degree_1', 
            'gpa_1': '1.1', 
            'previous_institution_2': 'previous_institution_2', 
            'degree_2': 'degree_2', 
            'gpa_2': '2.2', 
            'previous_institution_3': 'previous_institution_3', 
            'degree_3': 'degree_3', 
            'gpa_3': '3.3',
            'current_page': CURRENT_PAGE3,
            'next': NEXT,
            'tab': TAB3,
            'save': 'Save'
        }

        res3 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data3), content_type=ContentType, follow=True)
        messages3 = self.messages(res3)
        self.assertEqual(res3.status_code, 200)
        self.assertEqual(messages3[0], 'Success! Previous School Information Form saved.')

        data4 = {
            'status': '2', 
            'start_date': '2021-01-02', 
            'completion_date': '2022-01-02', 
            'graduation_date': '2022-05-02', 
            'comprehensive_exam_date': '2021-12-22',
            'thesis_title': 'title', 
            'funding_sources': 'school', 
            'total_funding_awarded': '2', 
            'taships': 'taships', 
            'current_role': 'researcher',
            'current_page': CURRENT_PAGE2,
            'next': NEXT,
            'tab': TAB2
        }

        res4 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data4), content_type=ContentType, follow=True)
        messages4 = self.messages(res4)
        self.assertEqual(messages4[0], 'Success! Student (firstname lastname, Student #: 90000888) created.')
        self.assertEqual(res4.status_code, 200)

        stud = api.get_student_by_sn(data1['student_number'])
        self.assertEqual(stud.first_name, data1['first_name'])
        self.assertEqual(stud.last_name, data1['last_name'])
        self.assertEqual(stud.student_number, data1['student_number'])
        self.assertEqual(stud.email, data1['email'])
        self.assertEqual(stud.date_of_birth, datetime.date(1990, 1, 1))
        self.assertEqual(stud.phone, data1['phone'])
        self.assertEqual(stud.sin, data1['sin'])
        self.assertEqual(stud.loa_months, int(data1['loa_months']))
        self.assertEqual(stud.loa_details, data1['loa_details'])
        self.assertTrue(stud.policy_85)
        self.assertEqual(stud.note, data1['note'])
        
        self.assertEqual(stud.status.id, int(data4['status']))
        self.assertEqual(stud.start_date, datetime.date(2021, 1, 2))
        self.assertEqual(stud.completion_date, datetime.date(2022, 1, 2))
        self.assertEqual(stud.graduation_date, datetime.date(2022, 5, 2))
        self.assertEqual(stud.comprehensive_exam_date, datetime.date(2021, 12, 22))
        self.assertEqual(stud.thesis_title, data4['thesis_title'])
        self.assertEqual(stud.funding_sources, data4['funding_sources'])
        self.assertEqual(stud.total_funding_awarded, data4['total_funding_awarded'])
        self.assertEqual(stud.taships, data4['taships'])
        self.assertEqual(stud.current_role, data4['current_role'])

        self.assertEqual(stud.previous_institution_1, data3['previous_institution_1'])
        self.assertEqual(stud.degree_1, data3['degree_1'])
        self.assertEqual(stud.gpa_1, data3['gpa_1'])
        self.assertEqual(stud.previous_institution_2, data3['previous_institution_2'])
        self.assertEqual(stud.degree_2, data3['degree_2'])
        self.assertEqual(stud.gpa_2, data3['gpa_2'])
        self.assertEqual(stud.previous_institution_3, data3['previous_institution_3'])
        self.assertEqual(stud.degree_3, data3['degree_3'])
        self.assertEqual(stud.gpa_3, data3['gpa_3'])
        

    def test_three_tabs_previous_school_info_success(self):
        print('- Test: create a student - three tabs - previous school info - success')
        self.login()

        TAB1 = 'basic_info'
        CURRENT_PAGE1 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB1)

        data1 = {
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
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1,
            'save': 'Save'
        }

        res1 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data1), content_type=ContentType, follow=True)
        messages1 = self.messages(res1)
        self.assertEqual(messages1[0], 'Success! Basic Information Form saved.')
        self.assertEqual(res1.status_code, 200)


        TAB2 = 'additional_info'
        CURRENT_PAGE2 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB2)

        data2 = {
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
            'current_page': CURRENT_PAGE2,
            'next': NEXT,
            'tab': TAB2,
            'save': 'Save'
        }
        res2 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data2), content_type=ContentType, follow=True)
        messages2 = self.messages(res2)
        self.assertEqual(messages2[0], 'Success! Additional Information Form saved.')
        self.assertEqual(res2.status_code, 200)


        TAB3 = 'previous_school_info'
        CURRENT_PAGE3 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB3)

        data3 = {
            'previous_institution_1': 'previous_institution_1', 
            'degree_1': 'degree_1', 
            'gpa_1': '1.1', 
            'previous_institution_2': 'previous_institution_2', 
            'degree_2': 'degree_2', 
            'gpa_2': '2.2', 
            'previous_institution_3': 'previous_institution_3', 
            'degree_3': 'degree_3', 
            'gpa_3': '3.3',
            'current_page': CURRENT_PAGE3,
            'next': NEXT,
            'tab': TAB3,
            'save': 'Save'
        }

        res3 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data3), content_type=ContentType, follow=True)
        messages3 = self.messages(res3)
        self.assertEqual(res3.status_code, 200)
        self.assertEqual(messages3[0], 'Success! Previous School Information Form saved.')

        data4 = {
            'previous_institution_1': 'previous_institution_11', 
            'degree_1': 'degree_11', 
            'gpa_1': '1.11', 
            'previous_institution_2': 'previous_institution_22', 
            'degree_2': 'degree_22', 
            'gpa_2': '2.22', 
            'previous_institution_3': 'previous_institution_33', 
            'degree_3': 'degree_33', 
            'gpa_3': '3.33',
            'current_page': CURRENT_PAGE3,
            'next': NEXT,
            'tab': TAB3
        }

        res4 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data4), content_type=ContentType, follow=True)
        messages4 = self.messages(res4)
        self.assertEqual(messages4[0], 'Success! Student (firstname lastname, Student #: 90000888) created.')
        self.assertEqual(res4.status_code, 200)

        stud = api.get_student_by_sn(data1['student_number'])
        self.assertEqual(stud.first_name, data1['first_name'])
        self.assertEqual(stud.last_name, data1['last_name'])
        self.assertEqual(stud.student_number, data1['student_number'])
        self.assertEqual(stud.email, data1['email'])
        self.assertEqual(stud.date_of_birth, datetime.date(1990, 1, 1))
        self.assertEqual(stud.phone, data1['phone'])
        self.assertEqual(stud.sin, data1['sin'])
        self.assertEqual(stud.loa_months, int(data1['loa_months']))
        self.assertEqual(stud.loa_details, data1['loa_details'])
        self.assertTrue(stud.policy_85)
        self.assertEqual(stud.note, data1['note'])
        
        self.assertEqual(stud.status.id, int(data2['status']))
        self.assertEqual(stud.start_date, datetime.date(2021, 1, 1))
        self.assertEqual(stud.completion_date, datetime.date(2022, 1, 1))
        self.assertEqual(stud.graduation_date, datetime.date(2022, 5, 1))
        self.assertEqual(stud.comprehensive_exam_date, datetime.date(2021, 12, 12))
        self.assertEqual(stud.thesis_title, data2['thesis_title'])
        self.assertEqual(stud.funding_sources, data2['funding_sources'])
        self.assertEqual(stud.total_funding_awarded, data2['total_funding_awarded'])
        self.assertEqual(stud.taships, data2['taships'])
        self.assertEqual(stud.current_role, data2['current_role'])

        self.assertEqual(stud.previous_institution_1, data4['previous_institution_1'])
        self.assertEqual(stud.degree_1, data4['degree_1'])
        self.assertEqual(stud.gpa_1, data4['gpa_1'])
        self.assertEqual(stud.previous_institution_2, data4['previous_institution_2'])
        self.assertEqual(stud.degree_2, data4['degree_2'])
        self.assertEqual(stud.gpa_2, data4['gpa_2'])
        self.assertEqual(stud.previous_institution_3, data4['previous_institution_3'])
        self.assertEqual(stud.degree_3, data4['degree_3'])
        self.assertEqual(stud.gpa_3, data4['gpa_3'])


    def test_cancel_student_create(self):
        print('- Test: cancel a student - create')
        self.login()

        TAB1 = 'basic_info'
        CURRENT_PAGE1 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB1)

        data1 = {
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
            'current_page': CURRENT_PAGE1,
            'next': NEXT,
            'tab': TAB1,
            'save': 'Save'
        }

        res1 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data1), content_type=ContentType, follow=True)
        messages1 = self.messages(res1)
        self.assertEqual(messages1[0], 'Success! Basic Information Form saved.')
        self.assertEqual(res1.status_code, 200)


        TAB2 = 'additional_info'
        CURRENT_PAGE2 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB2)

        data2 = {
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
            'current_page': CURRENT_PAGE2,
            'next': NEXT,
            'tab': TAB2,
            'save': 'Save'
        }
        res2 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data2), content_type=ContentType, follow=True)
        messages2 = self.messages(res2)
        self.assertEqual(messages2[0], 'Success! Additional Information Form saved.')
        self.assertEqual(res2.status_code, 200)


        TAB3 = 'previous_school_info'
        CURRENT_PAGE3 = '/admin/student/create/?next=/admin/students/all/?page=1&t={0}'.format(TAB3)

        data3 = {
            'previous_institution_1': 'previous_institution_1', 
            'degree_1': 'degree_1', 
            'gpa_1': '1.1', 
            'previous_institution_2': 'previous_institution_2', 
            'degree_2': 'degree_2', 
            'gpa_2': '2.2', 
            'previous_institution_3': 'previous_institution_3', 
            'degree_3': 'degree_3', 
            'gpa_3': '3.3',
            'current_page': CURRENT_PAGE3,
            'next': NEXT,
            'tab': TAB3,
            'save': 'Save'
        }

        res3 = self.client.post(reverse('gp_admin:create_student'), data=urlencode(data3), content_type=ContentType, follow=True)
        messages3 = self.messages(res3)
        self.assertEqual(res3.status_code, 200)
        self.assertEqual(messages3[0], 'Success! Previous School Information Form saved.')

        res4 = self.client.get(reverse('gp_admin:cancel_student') + '?next=' + NEXT, follow=True)
        self.assertEqual(res4.status_code, 200)
        
        res5 = self.client.get(reverse('gp_admin:create_student') + '?next=' + NEXT + '&t=basic_info', follow=True)
        self.assertEqual(res5.status_code, 200)
        self.assertFalse(res5.context['form'].is_bound)
        
        
# Edit Student


    def test_edit_student_page(self):
        print('- Test: edit a student - page')
        self.login()

        res = self.client.get(reverse('gp_admin:edit_student', args=[STUDENTS[0]]) + '?next=' + NEXT + '&t=basic_info', follow=True)
        self.assertEqual(res.status_code, 200)

        stud = res.context['stud']
        self.assertEqual(stud.id, 1)
        self.assertEqual(stud.first_name, 'John')
        self.assertEqual(stud.last_name, 'Doe')
        self.assertEqual(stud.student_number, '90000001')
        self.assertEqual(stud.email, 'john.doe@example.com')
        self.assertEqual(stud.date_of_birth, datetime.date(2001, 1, 1))
        self.assertEqual(stud.phone, '123-456-7890')
        self.assertEqual(stud.sin, '123 456 789')
        self.assertEqual(stud.loa_months, 16)
        self.assertEqual(stud.loa_details, 'LOA Details')
        self.assertTrue(stud.policy_85)
        self.assertEqual(stud.note, '<p>This is a note.</p>')
        
        self.assertEqual(stud.status.id, 1)
        self.assertEqual(stud.start_date, datetime.date(2020, 9, 21))
        self.assertEqual(stud.completion_date, datetime.date(2022, 12, 31))
        self.assertEqual(stud.graduation_date, datetime.date(2023, 4, 30))
        self.assertEqual(stud.comprehensive_exam_date, datetime.date(2022, 10, 1))
        self.assertEqual(stud.thesis_title, 'Thesis Title')
        self.assertEqual(stud.funding_sources, 'Funding Sources')
        self.assertEqual(stud.total_funding_awarded, 'Total Funcding Awarded')
        self.assertEqual(stud.taships, 'TAships')
        self.assertEqual(stud.current_role, 'Researcher at IBM')

        self.assertEqual(stud.previous_institution_1, 'UBC')
        self.assertEqual(stud.degree_1, 'B.Sc.')
        self.assertEqual(stud.gpa_1, '3.5')
        self.assertIsNone(stud.previous_institution_2)
        self.assertIsNone(stud.degree_2)
        self.assertIsNone(stud.gpa_2)
        self.assertIsNone(stud.previous_institution_3)
        self.assertIsNone(stud.degree_3)
        self.assertIsNone(stud.gpa_3)

        #self.assertFalse(res.context['form'].is_bound)
        self.assertEqual(res.context['info'], {'btn_label': 'Update', 'type': 'edit', 'path': 'students'})
        self.assertEqual(res.context['next'], NEXT)
        self.assertEqual(res.context['tab'], 'basic_info')
        self.assertEqual(res.context['tab_urls'], {'basic_info': '/admin/students/90000001/edit/?next=/admin/students/?page=1&t=basic_info', 'additional_info': '/admin/students/90000001/edit/?next=/admin/students/?page=1&t=additional_info', 'previous_school_info': '/admin/students/90000001/edit/?next=/admin/students/?page=1&t=previous_school_info'})


    def test_edit_student_missing_required_fields_first_name(self):
        print('- Test: edit a student - missing required fields - first name')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/students/{0}/edit/?next=/admin/students/?page=1&t={1}'.format(STUDENTS[0], TAB)
        
        data = {
            'first_name': '',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': 'email@example.com',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:edit_student', args=[STUDENTS[0]]), data=urlencode(data), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. FIRST NAME: This field is required.')
        self.assertEqual(res.status_code, 200)


    def test_edit_student_missing_required_fields_last_name(self):
        print('- Test: edit a student - missing required fields - last name')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/students/{0}/edit/?next=/admin/students/?page=1&t={1}'.format(STUDENTS[0], TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': '',
            'student_number': '90000222',
            'email': 'email@example.com',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:edit_student', args=[STUDENTS[0]]), data=urlencode(data), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. LAST NAME: This field is required.')
        self.assertEqual(res.status_code, 200)


    def test_edit_student_missing_required_fields_student_number(self):
        print('- Test: edit a student - missing required fields - student number')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/students/{0}/edit/?next=/admin/students/?page=1&t={1}'.format(STUDENTS[0], TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '',
            'email': 'email@example.com',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:edit_student', args=[STUDENTS[0]]), data=urlencode(data), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. STUDENT NUMBER: This field is required.')
        self.assertEqual(res.status_code, 200)


    def test_edit_student_missing_required_fields_email(self):
        print('- Test: edit a student - missing required fields - email')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/students/{0}/edit/?next=/admin/students/?page=1&t={1}'.format(STUDENTS[0], TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': '',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:edit_student', args=[STUDENTS[0]]), data=urlencode(data), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. EMAIL: This field is required.')
        self.assertEqual(res.status_code, 200)


    def test_edit_student_wrong_email(self):
        print('- Test: edit a student - wrong email')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/students/{0}/edit/?next=/admin/students/?page=1&t={1}'.format(STUDENTS[0], TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': 'email',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:edit_student', args=[STUDENTS[0]]), data=urlencode(data), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. EMAIL: Enter a valid email address.')
        self.assertEqual(res.status_code, 200)


    def test_edit_student_loa_months_min_failure(self):
        print('- Test: edit a student - loa months - min failure')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/students/{0}/edit/?next=/admin/students/?page=1&t={1}'.format(STUDENTS[0], TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': 'email@example.com',
            'loa_months': -1,
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:edit_student', args=[STUDENTS[0]]), data=urlencode(data), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. LOA MONTHS: Ensure this value is greater than or equal to 0.')
        self.assertEqual(res.status_code, 200)


    def test_edit_student_loa_months_max_failure(self):
        print('- Test: edit a student - loa months - max failure')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/students/{0}/edit/?next=/admin/students/?page=1&t={1}'.format(STUDENTS[0], TAB)
        
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'student_number': '90000222',
            'email': 'email@example.com',
            'loa_months': 201,
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:edit_student', args=[STUDENTS[0]]), data=urlencode(data), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. Form is invalid. LOA MONTHS: Ensure this value is less than or equal to 200.')
        self.assertEqual(res.status_code, 200)


    # Basic Information


    def test_edit_student_tab_error(self):
        print('- Test: edit a student - tab error')
        self.login()

        TAB = 'basic_infoa'
        CURRENT_PAGE = '/admin/students/{0}/edit/?next=/admin/students/all/?page=1&t={1}'.format(STUDENTS[0], TAB)

        data = {
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
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:edit_student', args=[STUDENTS[0]]), data=urlencode(data), content_type=ContentType)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'An error occurred. No valid tab.')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, CURRENT_PAGE)
        # self.assertRedirects(res, res.url)


    def test_edit_student_basic_info_only(self):
        print('- Test: edit a student - basic info only')
        self.login()

        TAB = 'basic_info'
        CURRENT_PAGE = '/admin/students/{0}/edit/?next=/admin/students/all/?page=1&t={1}'.format(STUDENTS[0], TAB)

        data = {
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
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:edit_student', args=[STUDENTS[0]]), data=urlencode(data), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! Student (firstname lastname, Student #: 90000888) updated.')
        self.assertEqual(res.status_code, 200)

        stud = api.get_student_by_sn(data['student_number'])
        self.assertEqual(stud.id, 1)
        self.assertEqual(stud.first_name, data['first_name'])
        self.assertEqual(stud.last_name, data['last_name'])
        self.assertEqual(stud.student_number, data['student_number'])
        self.assertEqual(stud.email, data['email'])
        self.assertEqual(stud.date_of_birth, datetime.date(1990, 1, 1))
        self.assertEqual(stud.phone, data['phone'])
        self.assertEqual(stud.sin, data['sin'])
        self.assertEqual(stud.loa_months, int(data['loa_months']))
        self.assertEqual(stud.loa_details, data['loa_details'])
        self.assertTrue(stud.policy_85)
        self.assertEqual(stud.note, data['note'])

        self.assertEqual(stud.status.id, 1)
        self.assertEqual(stud.start_date, datetime.date(2020, 9, 21))
        self.assertEqual(stud.completion_date, datetime.date(2022, 12, 31))
        self.assertEqual(stud.graduation_date, datetime.date(2023, 4, 30))
        self.assertEqual(stud.comprehensive_exam_date, datetime.date(2022, 10, 1))
        self.assertEqual(stud.thesis_title, 'Thesis Title')
        self.assertEqual(stud.funding_sources, 'Funding Sources')
        self.assertEqual(stud.total_funding_awarded, 'Total Funcding Awarded')
        self.assertEqual(stud.taships, 'TAships')
        self.assertEqual(stud.current_role, 'Researcher at IBM')

        self.assertEqual(stud.previous_institution_1, 'UBC')
        self.assertEqual(stud.degree_1, 'B.Sc.')
        self.assertEqual(stud.gpa_1, '3.5')
        self.assertIsNone(stud.previous_institution_2)
        self.assertIsNone(stud.degree_2)
        self.assertIsNone(stud.gpa_2)
        self.assertIsNone(stud.previous_institution_3)
        self.assertIsNone(stud.degree_3)
        self.assertIsNone(stud.gpa_3)
        


    def test_edit_student_additional_info_only(self):
        print('- Test: edit a student - additional info only')
        self.login()

        TAB = 'additional_info'
        CURRENT_PAGE = '/admin/students/{0}/edit/?next=/admin/students/all/?page=1&t={1}'.format(STUDENTS[0], TAB)

        data = {
            'status': '4', 
            'start_date': '2021-01-02', 
            'completion_date': '2022-01-02', 
            'graduation_date': '2022-05-02', 
            'comprehensive_exam_date': '2021-12-22',
            'thesis_title': 'title2', 
            'funding_sources': 'school2', 
            'total_funding_awarded': '22', 
            'taships': 'taships2', 
            'current_role': 'researcher2',
            'current_page': CURRENT_PAGE,
            'next': NEXT,
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:edit_student', args=[STUDENTS[0]]), data=urlencode(data), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! Student (John Doe, Student #: 90000001) updated.')
        self.assertEqual(res.status_code, 200)
        
        stud = api.get_student_by_sn(STUDENTS[0])
        self.assertEqual(stud.id, 1)
        self.assertEqual(stud.first_name, 'John')
        self.assertEqual(stud.last_name, 'Doe')
        self.assertEqual(stud.student_number, '90000001')
        self.assertEqual(stud.email, 'john.doe@example.com')
        self.assertEqual(stud.date_of_birth, datetime.date(2001, 1, 1))
        self.assertEqual(stud.phone, '123-456-7890')
        self.assertEqual(stud.sin, '123 456 789')
        self.assertEqual(stud.loa_months, 16)
        self.assertEqual(stud.loa_details, 'LOA Details')
        self.assertTrue(stud.policy_85)
        self.assertEqual(stud.note, '<p>This is a note.</p>')

        self.assertEqual(stud.status.id, int(data['status']))
        self.assertEqual(stud.start_date, datetime.date(2021, 1, 2))
        self.assertEqual(stud.completion_date, datetime.date(2022, 1, 2))
        self.assertEqual(stud.graduation_date, datetime.date(2022, 5, 2))
        self.assertEqual(stud.comprehensive_exam_date, datetime.date(2021, 12, 22))
        self.assertEqual(stud.thesis_title, data['thesis_title'])
        self.assertEqual(stud.funding_sources, data['funding_sources'])
        self.assertEqual(stud.total_funding_awarded, data['total_funding_awarded'])
        self.assertEqual(stud.taships, data['taships'])
        self.assertEqual(stud.current_role, data['current_role'])

        self.assertEqual(stud.previous_institution_1, 'UBC')
        self.assertEqual(stud.degree_1, 'B.Sc.')
        self.assertEqual(stud.gpa_1, '3.5')
        self.assertIsNone(stud.previous_institution_2)
        self.assertIsNone(stud.degree_2)
        self.assertIsNone(stud.gpa_2)
        self.assertIsNone(stud.previous_institution_3)
        self.assertIsNone(stud.degree_3)
        self.assertIsNone(stud.gpa_3)
        

    def test_edit_student_previous_school_info_only(self):
        print('- Test: edit a student - previous school info only')
        self.login()

        TAB = 'previous_school_info'
        CURRENT_PAGE = '/admin/students/{0}/edit/?next=/admin/students/all/?page=1&t={1}'.format(STUDENTS[0], TAB)

        data = {
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
            'tab': TAB
        }

        res = self.client.post(reverse('gp_admin:edit_student', args=[STUDENTS[0]]), data=urlencode(data), content_type=ContentType, follow=True)
        messages = self.messages(res)
        self.assertEqual(messages[0], 'Success! Student (John Doe, Student #: 90000001) updated.')
        self.assertEqual(res.status_code, 200)
        
        stud = api.get_student_by_sn(STUDENTS[0])
        self.assertEqual(stud.id, 1)
        self.assertEqual(stud.first_name, 'John')
        self.assertEqual(stud.last_name, 'Doe')
        self.assertEqual(stud.student_number, '90000001')
        self.assertEqual(stud.email, 'john.doe@example.com')
        self.assertEqual(stud.date_of_birth, datetime.date(2001, 1, 1))
        self.assertEqual(stud.phone, '123-456-7890')
        self.assertEqual(stud.sin, '123 456 789')
        self.assertEqual(stud.loa_months, 16)
        self.assertEqual(stud.loa_details, 'LOA Details')
        self.assertTrue(stud.policy_85)
        self.assertEqual(stud.note, '<p>This is a note.</p>')
        
        self.assertEqual(stud.status.id, 1)
        self.assertEqual(stud.start_date, datetime.date(2020, 9, 21))
        self.assertEqual(stud.completion_date, datetime.date(2022, 12, 31))
        self.assertEqual(stud.graduation_date, datetime.date(2023, 4, 30))
        self.assertEqual(stud.comprehensive_exam_date, datetime.date(2022, 10, 1))
        self.assertEqual(stud.thesis_title, 'Thesis Title')
        self.assertEqual(stud.funding_sources, 'Funding Sources')
        self.assertEqual(stud.total_funding_awarded, 'Total Funcding Awarded')
        self.assertEqual(stud.taships, 'TAships')
        self.assertEqual(stud.current_role, 'Researcher at IBM')

        self.assertEqual(stud.previous_institution_1, data['previous_institution_1'])
        self.assertEqual(stud.degree_1, data['degree_1'])
        self.assertEqual(stud.gpa_1, data['gpa_1'])
        self.assertEqual(stud.previous_institution_2, data['previous_institution_2'])
        self.assertEqual(stud.degree_2, data['degree_2'])
        self.assertEqual(stud.gpa_2, data['gpa_2'])
        self.assertEqual(stud.previous_institution_3, data['previous_institution_3'])
        self.assertEqual(stud.degree_3, data['degree_3'])
        self.assertEqual(stud.gpa_3, data['gpa_3'])