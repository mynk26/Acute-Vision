from django.urls import path
from .views import StudentAttendance,ModifyAttendanceList,ModifyAttendanceSelected,TakeAttendance,CheckAttendanceList

urlpatterns = [
    path('student/attendance/',StudentAttendance),
    path('teacher/checkattendance/',CheckAttendanceList),
    path('teacher/modifyattendance/',ModifyAttendanceList),
    path('teacher/modifyattendance/<int:pk>/',ModifyAttendanceSelected),
    path('teacher/takeattendance/',TakeAttendance)
]
