from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render, redirect
from .forms import SignUpForm,StudentProfileForm,TeacherProfileForm,LoginForm,StudentProfileUpdateForm
from .models import user_account,Student,Teacher
from section.models import Section

class Index(View):
    def get(self,request):
        return render(request,'index.html')

def SignUpView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            UserType = form.cleaned_data.get('user_type')
            instance = form.save(commit=False)
            if UserType == 'STUDENT':
                instance.is_teacher = False
                instance.is_student = True
                instance.is_pending = False
                instance.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('student/')
            elif UserType == 'TEACHER':
                instance.is_teacher = True
                instance.is_student = False
                instance.is_pending = True
                instance.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('teacher/')

    else:
        form = SignUpForm()
    return render(request, 'signup_form.html', {'form': form})


def StudentProfile(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Enrollment=request.user
            dep=instance.Department
            sem=instance.Semester
            sec=form.cleaned_data.get('Section')
            sec_name=str(dep)+'-'+str(sem)+str(sec)
            instance.Section=Section.objects.get(Section_Name=sec_name)
            instance.save()
            return redirect('../../Home/')
    else:
        form = StudentProfileForm()
    return render(request, 'StudentProfile.html', {'form': form})


def TeacherProfile(request):
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Id=request.user
            instance.save()
            return redirect('../../Home/')
    else:
        form = TeacherProfileForm()
    return render(request, 'TeacherProfile.html', {'form': form})

def LoginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('UserId')
            password=form.cleaned_data.get('Password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('../Home/')
            else:
                return HttpResponse("<script>window.location.href = './'; alert('Incorrect UserName/Password');</script>")

    else:
        form = LoginForm()
    return render(request,'LoginForm.html',{'form':form})


def HomePage(request):
    UserId = request.user
    try:
        User_account = user_account.objects.get(username=UserId)
    except:
        return HttpResponse('<script>window.location.href="../";alert("Not a User!!!!")</script>')
    if User_account.is_student:
        return render(request,'StudentHome.html')
    elif User_account.is_teacher:
        if User_account.is_pending:
            return render(request,'TeacherHome0.html')
        else:
            return render(request,'TeacherHome.html')
    else:
        return HttpResponse('<script>window.location.href="../";alert("Not Identified as teacher or student")</script>')

def StudentProfileUpdate(request):
    UserId = request.user
    User_account = user_account.objects.get(username=UserId)
    if User_account.is_student:
        if request.method == 'POST':
            form = StudentProfileUpdateForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.Enrollment=request.user
                profile = Student.objects.get(Enrollment=instance.Enrollment)
                instance.Department=profile.Department
                instance.Semester=profile.Semester
                instance.Year=profile.Year
                instance.Section=profile.Section
                instance.save()
                return HttpResponse("<script>window.location.href='../../Home/MainPage';alert('Profile Updated');</script>")
        else:
            try:
                student = Student.objects.get(Enrollment=request.user)
                form = StudentProfileUpdateForm(instance=student)
                form.fields['Year'].widget.attrs['readonly']=True
                form.fields['Semester'].widget.attrs['readonly']=True
                form.fields['Department'].widget.attrs['readonly']=True
                form.fields['Section'].widget.attrs['readonly']=True
                form.fields['Department'].initial = str(student.Department)
                form.fields['Section'].initial = str(student.Section)
            except:
                return HttpResponse("<script>window.top.location.href = '../../signup/student/'; alert('add your profile');</script>")
        return render(request,'StudentProfile.html',{'form':form})
    return HttpResponse("<script>alert('Not a Student');</script>")


def TeacherProfileUpdate(request):
    if request.user.is_teacher:
        if request.method == 'POST':
            form = TeacherProfileForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.Id=request.user
                instance.save()
                return HttpResponse("<script>window.location.href='../../Home/MainPage';alert('Profile Updated Teacher');</script>")
        else:
            try:
                teacher = Teacher.objects.get(Id=request.user)
                form = TeacherProfileForm(instance=teacher)
            except:
                return HttpResponse("<script>window.top.location.href = '../../signup/teacher/'; alert('add your profile');</script>")
        return render(request,'TeacherProfile.html',{'form':form})
    return HttpResponse("<script>window.location.href = '../../Home';alert('Not a Teacher);</script>")

def MainPage(request):
    if request.user.is_student:
        try:
            profile = Student.objects.get(Enrollment=request.user)
        except:
            return HttpResponse("<script>window.top.location.href = '../../signup/student/'; alert('add your profile');</script>")
    elif request.user.is_teacher:
        try:
            profile = Teacher.objects.get(Id=request.user)
        except:
            return HttpResponse("<script>window.top.location.href = '../../signup/teacher/'; alert('add your profile');</script>")
    return render(request,'MainPage.html',{'name':profile.Name})

def logout_request(request):
    logout(request)
    return HttpResponse("<script>alert('Logged out successfully!');window.location.href = '../'</script>")
