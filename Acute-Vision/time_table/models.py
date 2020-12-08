from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
#from section.models import Section
#from account.models import Teacher
# Create your models here.
class Subject(models.Model):
    Department_List = (('CSE', 'CSE'),('IT','IT'),)
    Subject_Code = models.CharField(max_length = 10,primary_key = True)
    Subject_Name = models.CharField(max_length = 50)
    Semester = models.IntegerField(default=1,validators=[MaxValueValidator(8), MinValueValidator(1)])
    Department = models.CharField(max_length=10, choices=Department_List)
#class Time_Table(models.Model):
#    Day_List = (('MONDAY','MONDAY'),('TUESDAY','TUESDAY'),('WEDNESDAY','WEDNESDAY'),('THURSDAY','THURSDAY'),('FRIDAY','FRIDAY'),('SATURDAY','SATURDAY'))
#    Day = models.CharField(max_length=10, choices=Day_List)
#    Time = models.TimeField()
#    Section = models.ForeignKey(Section,on_delete = models.SET_NULL,null=True)
#    Teacher = models.ForeignKey(Teacher,on_delete = models.SET_NULL,null=True)
#    Subject = models.ForeignKey(Subject,on_delete = models.SET_NULL,null=True)
