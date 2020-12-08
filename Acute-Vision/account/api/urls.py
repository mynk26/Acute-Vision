from django.urls import path
from .views import LoginView,RegisterView,TeacherProfileView,StudentProfileView

urlpatterns = [
    path('login',LoginView.as_view(),name='LoginView'),
    path('register',RegisterView.as_view(),name='RegisterView'),
    path('profile/teacher',TeacherProfileView.as_view(),name='TeacherProfileView'),
    path('profile/student',StudentProfileView.as_view(),name='StudentProfileView'),
    path('profile/student/<str:username>',StudentProfileView.as_view(),name='StudentProfileView'),
    path('profile/teacher/<str:id>', TeacherProfileView.as_view(), name='TeacherProfileView'),
]
