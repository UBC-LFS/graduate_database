# Generated by Django 4.1.1 on 2022-10-25 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gp_admin', '0005_alter_student_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='hashcode',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='json',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
