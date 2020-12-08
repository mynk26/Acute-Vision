from django.urls import path
from .views import Subject_List

urlpatterns = [
    path('teacher/subject/<str:department>/<str:semester>',Subject_List.as_view(),name='SubjectListView based on department and section'),
]
