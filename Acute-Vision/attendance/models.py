from django.db import models
from account.models import Student
from section.models import Section
from time_table.models import Subject

# Create your models here.

class Attendance(models.Model):
    Status_List = (('P','P'),('A','A'))
    Enrollment = models.ForeignKey(Student,on_delete = models.CASCADE)
    Subject_Code = models.ForeignKey(Subject,on_delete = models.CASCADE)
    Section = models.ForeignKey(Section,on_delete = models.SET_NULL, null = True)
    Date = models.DateField()
    Status = models.CharField(max_length=1,choices = Status_List)
