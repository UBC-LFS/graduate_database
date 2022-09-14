from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator


# User

class Role(models.Model):
    SUPERADMIN = 'Superadmin'
    ADMIN = 'Admin'
    SUPERVISOR = 'Supervisor'
    GUEST = 'Guest'

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta: 
        ordering = ['pk']

    def __str__(self): 
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Role, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    preferred_name = models.CharField(max_length=150, null=True, blank=True)
    roles = models.ManyToManyField(Role)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username



# Preparation


class Status(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['name', 'pk']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Status, self).save(*args, **kwargs)


class Title(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['name', 'pk']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Title, self).save(*args, **kwargs)


class Position(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['name', 'pk']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Position, self).save(*args, **kwargs)


class Professor_Role(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Professor_Role, self).save(*args, **kwargs)


class Program(models.Model):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['name', 'code', 'pk']

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.code)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Program, self).save(*args, **kwargs)


# Data Tables


class Student(models.Model):
    GENDER_CHOICES = [ ('F', 'Female'), ('M', 'Male') ]
    NATIONALITY_CHOICES = [ ('C', 'CDN'), ('P', 'PERM'), ('S', 'STUV') ]

    last_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, null=True, blank=True)
    student_number = models.CharField(max_length=8, unique=True)
    email = models.CharField(max_length=150, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_work = models.CharField(max_length=20, null=True, blank=True)
    phone_home = models.CharField(max_length=20, null=True, blank=True)

    address = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    province = models.CharField(max_length=150, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=150, null=True, blank=True)
    perm_address = models.CharField(max_length=150, null=True, blank=True)

    foreign_domestic = models.CharField(max_length=1, choices=NATIONALITY_CHOICES, null=True, blank=True)
    sin = models.CharField(max_length=20, null=True, blank=True)
    
    current_degree = models.CharField(max_length=150, null=True, blank=True)
    program_code = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=150, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    loa_months = models.IntegerField(null=True, blank=True)
    loa_details = models.CharField(max_length=150, null=True, blank=True)

    previous_institution_1 = models.CharField(max_length=150, null=True, blank=True)
    degree_1 = models.CharField(max_length=50, null=True, blank=True)
    gpa_1 = models.CharField(max_length=20, null=True, blank=True)
    previous_institution_2 = models.CharField(max_length=150, null=True, blank=True)
    degree_2 = models.CharField(max_length=50, null=True, blank=True)
    gpa_2 = models.CharField(max_length=20, null=True, blank=True)
    previous_institution_3 = models.CharField(max_length=150, null=True, blank=True)
    degree_3 = models.CharField(max_length=50, null=True, blank=True)
    gpa_3 = models.CharField(max_length=20, null=True, blank=True)

    policy_85 = models.BooleanField(default=False)

    note = models.TextField(null=True, blank=True)

    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return '{0} {1}'.format(self.last_name, self.first_name)

    def get_full_name(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)


class Professor(models.Model):
    last_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.CharField(max_length=254, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=150, null=True, blank=True)
    fax = models.CharField(max_length=150, null=True, blank=True)
    office = models.CharField(max_length=150, null=True, blank=True)

    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return '{0} {1}'.format(self.last_name, self.first_name)

    def get_full_name(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)


class Supervision(models.Model):
    ''' To make a relationship bewteen students and professors '''

    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True)
    professor_role = models.ForeignKey(Professor_Role, on_delete=models.SET_NULL, null=True, blank=True)

    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        unique_together = (('student', 'professor'))


class Comprehensive_Exam(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    exam_date = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['student__last_name', 'student__first_name', 'exam_date']


class Reminder_Inbox(models.Model):
    ''' Send a reminder email to students '''
    comp_exam = models.ForeignKey(Comprehensive_Exam, on_delete=models.CASCADE)
    sender = models.CharField(max_length=150)
    receiver = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    message = models.TextField()
    type = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']


class Reminder(models.Model):
    ''' Admins can save an email message and title '''
    title = models.CharField(max_length=150)
    message = models.TextField()
    type = models.CharField(max_length=150, unique=True)
    month = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(200)]
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        ordering = ['pk']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.type)
        super(Reminder, self).save(*args, **kwargs)


class SIS_Student(models.Model):
    student_number = models.CharField(max_length=8, unique=True)
    json = models.JSONField()
    hashcode = models.CharField(max_length=255)

    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['json__surname', 'json__given_name']

    def __str__(self):
        return '{0} {1}'.format(self.id, self.student_number)

