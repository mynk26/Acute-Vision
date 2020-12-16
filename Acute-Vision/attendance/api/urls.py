from django.urls import path
from .views import StudentAttendanceList,ModifyAttendanceList,CheckAttendance,TakeAttendance,LoadFace

urlpatterns = [
    path('student/<str:username>',StudentAttendanceList.as_view(),name='StudentAttendanceView'),
    path('student', StudentAttendanceList.as_view(), name='StudentAttendanceView Based on Section'),
    path('teacher/modifyattendance/<str:date>/<str:section>/<str:subject_code>',ModifyAttendanceList.as_view(),name='ModifyAttendacneView'),
    path('teacher/modifyattendance', ModifyAttendanceList.as_view(),name='ModifyAttendacneView'),
    path('teacher/checkattendance/<str:section>/<str:subject_code>/<str:from_date>/<str:to_date>',CheckAttendance.as_view(),name='CheckAttendaceView'),
    path('teacher/takeattendance/<str:section>/<str:subject_code>/<str:class_id>',TakeAttendance.as_view(),name='TakeAttendanceView'),
    path('teacher/LoadFace',LoadFace.as_view(),name='Load Face Data')
]
