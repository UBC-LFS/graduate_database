# Generated by Django 4.1.1 on 2022-09-13 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp_admin', '0003_rename_reminder_setup_setup_reminder'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Setup_Reminder',
            new_name='Reminder',
        ),
    ]