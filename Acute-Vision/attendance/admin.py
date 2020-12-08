from django.contrib import admin
from .models import Attendance



@admin.register(Attendance)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('Enrollment','Subject_Code','Section','Date','Status')
