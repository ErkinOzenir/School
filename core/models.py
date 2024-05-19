from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    # Overriding the related_name for groups and user_permissions to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Group(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('elementary', 'Elementary'),
        # Add other levels here
    ]
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    code = models.CharField(max_length=10, unique=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teaching_groups')
    lessons_per_week = models.IntegerField()
    lesson_time = models.TimeField()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    progress = models.FloatField(default=0.0)

class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lessons')
    topic = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    is_online = models.BooleanField(default=True)

class Homework(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='homeworks')
    due_date = models.DateField()
    description = models.TextField()

class Exercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises')
    question = models.CharField(max_length=255)
    options = models.JSONField()
    correct_option = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

class Topic(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    pdf = models.FileField(upload_to='topics/')
