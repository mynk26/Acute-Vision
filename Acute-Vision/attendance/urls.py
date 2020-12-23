from django.urls import path
from .views import StudentCurrentAttendance,StudentAttendance,ModifyAttendanceList,ModifyAttendanceSelected,TakeAttendance,CheckAttendanceList

urlpatterns = [
    path('student/attendance/',StudentCurrentAttendance),
    path('student/attendance/previous',StudentAttendance),
    path('teacher/checkattendance/',CheckAttendanceList),
    path('teacher/modifyattendance/',ModifyAttendanceList),
    path('teacher/modifyattendance/<int:pk>/',ModifyAttendanceSelected),
    path('teacher/takeattendance/',TakeAttendance)
]
