# Generated by Django 4.1.1 on 2022-09-21 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp_admin', '0003_rename_end_date_student_completion_date_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reminder_Inbox',
            new_name='Sent_Reminder',
        ),
    ]
