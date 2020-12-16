from django.contrib import admin
from .models import user_account,Student,Teacher,FaceData



@admin.register(user_account)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('is_student','is_teacher','is_pending','username')


admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(FaceData)
