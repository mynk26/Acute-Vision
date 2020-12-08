from django.urls import path
from .views import Index,SignUpView,TeacherProfile,StudentProfile,LoginPage,HomePage,StudentProfileUpdate,TeacherProfileUpdate,logout_request

urlpatterns = [
    path('',Index.as_view()),
    path('signup/',SignUpView),
    path('signup/teacher/',TeacherProfile),
    path('signup/student/',StudentProfile),
    path('login/',LoginPage),
    path('logout/',logout_request),
    path('Home/',HomePage),
    path('student/profile/',StudentProfileUpdate),
    path('teacher/profile/',TeacherProfileUpdate),
]
