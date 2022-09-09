# Generated by Django 4.0.6 on 2022-09-09 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['name', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='Professor_Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['name', 'code', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='SIS_Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_number', models.CharField(max_length=8, unique=True)),
                ('json', models.JSONField()),
                ('hashcode', models.CharField(max_length=255)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['json__surname', 'json__given_name'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=150)),
                ('first_name', models.CharField(max_length=150)),
                ('middle_name', models.CharField(blank=True, max_length=150, null=True)),
                ('student_number', models.CharField(max_length=8, unique=True)),
                ('email', models.CharField(max_length=150, unique=True)),
                ('gender', models.CharField(blank=True, choices=[('F', 'Female'), ('M', 'Male')], max_length=1, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('phone_work', models.CharField(blank=True, max_length=20, null=True)),
                ('phone_home', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('city', models.CharField(blank=True, max_length=150, null=True)),
                ('province', models.CharField(blank=True, max_length=150, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True)),
                ('country', models.CharField(blank=True, max_length=150, null=True)),
                ('perm_address', models.CharField(blank=True, max_length=150, null=True)),
                ('foreign_domestic', models.CharField(blank=True, choices=[('C', 'CDN'), ('P', 'PERM'), ('S', 'STUV')], max_length=1, null=True)),
                ('sin', models.CharField(blank=True, max_length=20, null=True)),
                ('current_degree', models.CharField(blank=True, max_length=150, null=True)),
                ('program_code', models.CharField(blank=True, max_length=20, null=True)),
                ('status', models.CharField(blank=True, max_length=150, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('loa_months', models.IntegerField(blank=True, null=True)),
                ('loa_details', models.CharField(blank=True, max_length=150, null=True)),
                ('previous_institution_1', models.CharField(blank=True, max_length=150, null=True)),
                ('degree_1', models.CharField(blank=True, max_length=50, null=True)),
                ('gpa_1', models.CharField(blank=True, max_length=20, null=True)),
                ('previous_institution_2', models.CharField(blank=True, max_length=150, null=True)),
                ('degree_2', models.CharField(blank=True, max_length=50, null=True)),
                ('gpa_2', models.CharField(blank=True, max_length=20, null=True)),
                ('previous_institution_3', models.CharField(blank=True, max_length=150, null=True)),
                ('degree_3', models.CharField(blank=True, max_length=50, null=True)),
                ('gpa_3', models.CharField(blank=True, max_length=20, null=True)),
                ('policy_85', models.BooleanField(default=False)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['name', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='Comprehensive_Exam',
            fields=[
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='gp_admin.student')),
                ('exam_date', models.DateField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['student__last_name', 'student__first_name', 'exam_date'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('preferred_name', models.CharField(blank=True, max_length=150, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('roles', models.ManyToManyField(to='gp_admin.role')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=150)),
                ('first_name', models.CharField(max_length=150)),
                ('email', models.CharField(blank=True, max_length=254, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=150, null=True)),
                ('fax', models.CharField(blank=True, max_length=150, null=True)),
                ('office', models.CharField(blank=True, max_length=150, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gp_admin.position')),
                ('program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gp_admin.program')),
                ('title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gp_admin.title')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Supervision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('professor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gp_admin.professor')),
                ('professor_role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gp_admin.professor_role')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gp_admin.student')),
            ],
            options={
                'unique_together': {('student', 'professor')},
            },
        ),
        migrations.CreateModel(
            name='Exam_Reminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=150)),
                ('receiver', models.CharField(max_length=150)),
                ('title', models.CharField(max_length=150)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comp_exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gp_admin.comprehensive_exam')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
    ]