from django.db import models


# Create your models here.
class Section(models.Model):
    Section_Name = models.CharField(max_length = 50,primary_key=True)

class Class(models.Model):
    Camera_Id = models.CharField(max_length=50)
    Class_Number = models.CharField(max_length = 10,primary_key=True)
