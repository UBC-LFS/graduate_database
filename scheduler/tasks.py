from django.conf import settings
import os
from os import listdir
from os.path import isfile, join
import json
import hashlib
from datetime import datetime
from django.conf import settings
from pathlib import Path
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.core.mail import EmailMultiAlternatives

from apscheduler.schedulers.background import BackgroundScheduler
import xlrd
from openpyxl import load_workbook
from deepdiff import DeepDiff, DeepHash

from gp_admin import api

from gp_admin.models import Student, Sent_Reminder

#BASE_DIR = Path(__file__).resolve().parent.parent.parent
#PATH = os.path.join(BASE_DIR, 'playground', 'data')
PATH = settings.GRAD_DB_SIS_STUDENTS_DIR


HEADERS = [
    'STUD_NO', 'GIVEN_NAME', 'PREFERRED_NAME', 'MIDDLE_NAME', 'SURNAME', 'EMAIL_ADDRESS', 'GENDER', 
    'DEGR_PGM_CD', 'SPEC1_PRIM_SUBJ_CD',
    'ADDR1', 'ADDR2', 'CITY', 'PROVINCE_STATE', 'COUNTRY_CD', 'COUNTRY', 'POSTAL_CD',
    'COUNTRY_OF_CITIZENSHIP', 'CITIZENSHIP', 'VISA_TYPE_CD', 'DOM_INTL'
]


def get_item(row):
    stud_no = str( int(row[0].value) )
    item = {
        'stud_no': stud_no if len(stud_no) > 0 else None,
        'degr_pgm_cd': row[1].value if row[1].value else None,
        'spec1_prim_subj_cd': row[2].value if row[2].value else None,
        'given_name': row[3].value if row[3].value else None,
        'preferred_name': row[4].value if row[4].value else None,
        'middle_name': row[5].value if row[5].value else None,
        'surname': row[6].value if row[6].value else None,
        'addr1': row[7].value if row[7].value else None,
        'addr2': row[8].value if row[8].value else None,
        'city': row[9].value if row[9].value else None,
        'province_state': row[10].value if row[10].value else None,
        'country_cd': row[11].value if row[11].value else None,
        'country': row[12].value if row[12].value else None,
        'postal_cd': row[13].value if row[13].value else None,
        'email_address': row[14].value if row[14].value else None,
        'gender': row[15].value if row[15].value else None,
        'country_of_citizenship': row[16].value if row[16].value else None,
        'citizenship': row[17].value if row[17].value else None,
        'visa_type_cd': row[18].value if row[18].value else None,
        'dom_intl': row[19].value if row[19].value else None
    }
    
    return stud_no, item


def check_column_headers(row):
    if len(row) != len(HEADERS):
        return False
    
    for col in row:
        if col.value not in HEADERS:
            return False
    return True
        

def read_old_excel(f, stud_nos, items):
    FILE_DIR = os.path.join(PATH, f)
    book = xlrd.open_workbook(FILE_DIR)
    sheet = book.sheet_by_index(0)
    
    for i in range(sheet.nrows):
        if i == 0:
            check_column_headers(sheet.row(0))
            
        else:
            stud_no, item = get_item(sheet.row(i))
            if stud_no not in stud_nos:
                stud_nos.append(stud_no)
                items.append(item)
    
    return stud_nos, items


def read_new_excel(f, stud_nos, items):
    FILE_DIR = os.path.join(PATH, f)
    book = load_workbook(FILE_DIR)
    sheet = book.active
    
    i = 0
    for row in book.active.rows:
        if i == 0:
            check_column_headers(row)
        else:
            stud_no, item = get_item(row)
            if stud_no not in stud_nos:
                stud_nos.append(stud_no)
                items.append(item)
        
        i += 1
    
    return stud_nos, items

def get_sis_students():
    stud_nos = []
    items = []
    for f in listdir(PATH):
        if isfile( join(PATH, f) ):
            ext = os.path.splitext(f)[-1].lower()
            if ext == '.xls':
                stud_nos, items = read_old_excel(f, stud_nos, items)
                print('===== File 1:', f, len(items))
            
            elif ext in ['.xlsx', '.xlsm', '.xltx', '.xltm']:
                stud_nos, items = read_new_excel(f, stud_nos, items)
                print('===== File 2:', f, len(items))
               
    print(len(stud_nos), len(items))

    old_stduents = Student.objects.all()
    old_stduent_nos = [ s.student_number for s in old_stduents ]
    
    create_students = []
    update_students = []
    new_set = set()

    for item in items:
        new_set.add(item['stud_no'])
        hashcode = hashlib.sha256( json.dumps(item).encode('utf-8') ).hexdigest()
        
        if item['stud_no'] in old_stduent_nos:
            student_filtered = Student.objects.filter(student_number=item['stud_no'])

            if student_filtered.exists() and hashcode != student_filtered.first().hashcode:
                stud = student_filtered.first()
                
                stud.first_name = item['given_name']
                stud.last_name = item['surname']
                stud.student_number = item['stud_no']
                stud.email = item['email_address']
                stud.updated_on = datetime.today()
                stud.json = item
                stud.hashcode = hashcode
                stud.sis_updated_on = datetime.today()

                update_students.append(stud)
        else:
            create_students.append( Student(
                first_name = item['given_name'],
                last_name = item['surname'],
                student_number = item['stud_no'],
                email = item['email_address'],
                json = item, 
                hashcode = hashcode,
                sis_created_on = datetime.today(),
                sis_updated_on = datetime.today()
            ) )

    # Bulk delete
    old_set = set(old_stduent_nos)
    delete_student_nos = list(old_set - new_set)
    print('delete_students', len(delete_student_nos))
    if len(delete_student_nos) > 0:
        for student_no in delete_student_nos:
            print(student_no)
            deleted = Student.objects.filter(student_number=student_no).delete()
            print(deleted)

    # Bulk update
    print('update_students', len(update_students))
    if len(update_students) > 0:
        updated = Student.objects.bulk_update(update_students, [
            'first_name', 
            'last_name', 
            'student_number', 
            'email', 
            'updated_on',
            'json', 
            'hashcode', 
            'sis_updated_on'
        ])
        print('===== updated', updated)

    # Bulk create
    print('create_students', len(create_students))
    if len(create_students) > 0:
        created = Student.objects.bulk_create(create_students)
        print('===== created', created)


def send_reminders():
    today = datetime.today().date()
    reminders = api.get_reminders()
    students = api.get_students()
    sender = settings.EMAIL_FROM
    for stud in students:
        receiver = '{0} {1} <{2}>'.format(stud.first_name, stud.last_name, stud.email)
        
        for rem in reminders:
            new_date = stud.start_date + relativedelta(months=rem.months)
            if new_date == today:
                message = rem.message.format(
                    stud.first_name,
                    stud.last_name,
                    stud.student_number,
                    stud.comprehensive_exam_date
                )

                msg = EmailMultiAlternatives(rem.title, message, sender, [receiver])
                msg.attach_alternative(message, "text/html")
                msg.send()

                sent = Sent_Reminder.objects.create(
                    student = stud,
                    sender = sender,
                    receiver = receiver,
                    title = rem.title,
                    message = message,
                    type = rem.type
                )
                print('Success!', stud.id, stud.start_date, new_date, new_date == today)


def run():
    print('Scheduling tasks running...')
    # scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    
    # Get SIS students
    # scheduler.add_job(get_sis_students, 'cron', day_of_week='mon-sun', hour=7, minute='0')

    # Send Reminders
    # scheduler.add_job(send_reminders, 'cron', day_of_week='mon-sun', hour=15, minute='0')
    
    # scheduler.start()