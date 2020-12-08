from django import forms
from django.forms import ModelForm,Form
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth.models import User

from account.models import user_account,Student,Teacher
from time_table.models import Subject

class SignUpForm(UserCreationForm):
    UserType = (('',''),('STUDENT','STUDENT'),('TEACHER','TEACHER'),)
    user_type = forms.ChoiceField(choices=UserType)
    class Meta:
        model = user_account
        fields = ('user_type','username', 'password1', 'password2')

class StudentProfileForm(ModelForm):
    Section_List = (('',''),('A','A'),('B','B'),('C','C'))
    Section = forms.ChoiceField(choices=Section_List)
    class Meta:
        model = Student
        fields = ('Name','Mobile','Email','Year','Semester','Department')

class StudentProfileUpdateForm(ModelForm):
    Department = forms.CharField(max_length=30)
    Section = forms.CharField(max_length=30)
    class Meta:
        model = Student
        fields = ('Name','Mobile','Email','Year','Semester')

class TeacherProfileForm(ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"
        exclude=('Id',)


class LoginForm(Form):
    UserId=forms.CharField(max_length=150)
    Password=forms.CharField(max_length=32,widget=forms.PasswordInput)
