# Generated by Django 4.1.1 on 2022-09-21 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gp_admin', '0005_rename_month_reminder_months'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sent_reminder',
            name='comp_exam',
        ),
        migrations.AddField(
            model_name='sent_reminder',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gp_admin.student'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Comprehensive_Exam',
        ),
    ]