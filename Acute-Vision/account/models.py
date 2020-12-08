from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
from section.models import Section
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class user_account(AbstractUser):
    username = models.CharField(max_length=254, unique=True, db_index=True, primary_key=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True)

class Student(models.Model):
    Department_List = (('CSE','CSE'),('IT','IT'),)
    Name = models.CharField(max_length = 50)
    Mobile = models.CharField(max_length=13)
    Email = models.EmailField(max_length=254,null=True)
    Year = models.IntegerField(default=1,
        validators=[MaxValueValidator(4), MinValueValidator(1)]
    )
    Semester = models.IntegerField(default=1,
        validators=[MaxValueValidator(8), MinValueValidator(1)]
     )
    Department  = models.CharField(max_length=10, choices=Department_List)
    Enrollment = models.OneToOneField(user_account, on_delete=models.CASCADE, primary_key=True)
    Section = models.ForeignKey(Section,on_delete=models.SET_NULL,null = True)

class Teacher(models.Model):
    Name = models.CharField(max_length = 50)
    Email = models.CharField(max_length = 50,null=True)
    Mobile = models.CharField(max_length=13)
    Id = models.OneToOneField(user_account, on_delete=models.CASCADE, primary_key=True)
