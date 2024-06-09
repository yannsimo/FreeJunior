from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission
from django.template.defaultfilters import slugify

class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True)
    contact_info = models.TextField()

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Specialty(models.Model):
    name = models.CharField(max_length=100)
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

class Program(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='programs')

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=255)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

class StudentManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
class Student(AbstractBaseUser):
    STUDY_LEVEL_CHOICES = [
        ('Bac+3', 'Bac+3'),
        ('Bac+4', 'Bac+4'),
        ('Bac+5', 'Bac+5'),
        ('Bac+6', 'Bac+6'),
        ('Bac+7', 'Bac+7'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=128, null=True)
    study_level = models.CharField(max_length=5, choices=STUDY_LEVEL_CHOICES, null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students', null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='students', null=True)
    related_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='student_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='student_set', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = StudentManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Description(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='description')
    description = models.TextField(null=True)

class Photo(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='photo')
    photo = models.ImageField(upload_to='student_photos/', null=True)

class CV(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='cv')
    cv = models.FileField(upload_to='student_cvs/', blank=True, null=True)

class Mission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='missions')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='missions')

    def __str__(self):
        return self.title

class Review(models.Model):
    rating = models.IntegerField()
    comment = models.TextField()
    mission = models.ForeignKey(Mission, related_name='reviews', on_delete=models.CASCADE)

    def __str__(self):
        return f"Review for {self.mission.title} by {self.mission.student.first_name}"

class Comment(models.Model):
    STATUS_VISIBLE = 'visible'
    STATUS_HIDDEN = 'hidden'
    STATUS_MODERATED = 'moderated'

    STATUS_CHOICES = (
        (STATUS_VISIBLE, 'Visible'),
        (STATUS_HIDDEN, 'Hidden'),
        (STATUS_MODERATED, 'Moderated'),
    )
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='comments')
    company_name = models.CharField(max_length=100)
    mission_title = models.CharField(max_length=100)
    text = models.TextField()
    status = models.CharField(max_length=20, default=STATUS_VISIBLE, choices=STATUS_CHOICES)
    moderation_text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {} (status={})'.format(self.company_name, self.text[:20], self.status)
