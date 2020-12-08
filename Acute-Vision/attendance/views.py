from django.http import HttpResponse
from django.core import serializers
import json
from django.shortcuts import render
from account.models import user_account,Student
from section.models import Section
from .models import Attendance
from django.conf import settings
from .forms import TakeAttendanceForm,ModifyAttendanceForm,ModifyAttendanceSelectedForm,StudentAttendanceForm,CheckAttendanceForm
User = settings.AUTH_USER_MODEL
# Create your views here.
def StudentAttendance(request):
    UserId = request.user
    User_account = user_account.objects.get(username=UserId)
    if User_account.is_student:
        if request.method=='POST':
            form =StudentAttendanceForm(request.POST)
            if form.is_valid():
                semester = form.cleaned_data.get('Semester')
                section = form.cleaned_data.get('Section')
                student_obj = Student.objects.get(Enrollment=UserId)
                section_name=Section.objects.get(Section_Name='CSE-'+str(semester)+str(section))
                result = Attendance.objects.filter(Enrollment=student_obj,Section=section_name)
                result_json = serializers.serialize('json',result)
                result_objs = json.loads(result_json)
                return render(request,'StudentAttendance.html',{'results':reversed(result_objs)})
        form = StudentAttendanceForm()
        return render(request,'StudentAttendance0.html',{'form':form})
    return HttpResponse("<script>window.location.href = '../../Home';alert('Not a Student');</script>")


def ModifyAttendanceList(request):
    UserId = request.user
    User_Type = user_account.objects.get(username=UserId)
    if User_Type.is_teacher and not User_Type.is_pending:
        if request.method == 'POST':
            form = ModifyAttendanceForm(request.POST)
            if form.is_valid():
                Section = str(form.cleaned_data.get('Section').Section_Name)
                Subject_Code = str(form.cleaned_data.get('Subject').Subject_Code)
                Date = str(form.cleaned_data.get('Date'))
                result = Attendance.objects.filter(Section=Section,Subject_Code=Subject_Code,Date=Date)
                result_json = serializers.serialize('json',result)
                result_objs=json.loads(result_json)
                return render(request,'ModifyAttendanceList.html',{'results':result_objs})
        form = ModifyAttendanceForm()
        return render(request,'ModifyAttendance.html',{'form':form})
    return HttpResponse("<script>window.location.href = '../../Home';alert('Not Verified');</script>")

def ModifyAttendanceSelected(request,pk):
    UserId = request.user
    User_account = user_account.objects.get(username=UserId)
    if User_account.is_teacher and not User_account.is_pending:
        if request.method == 'POST':
            form = ModifyAttendanceSelectedForm(request.POST)
            if form.is_valid():
                instance = Attendance.objects.get(pk=pk)
                instance.Status=form.cleaned_data.get('Status')
                instance.save()
                Section = instance.Section
                Subject_Code = instance.Subject_Code
                Date = instance.Date
                result = Attendance.objects.filter(Section=Section,Subject_Code=Subject_Code,Date=Date)
                result_json = serializers.serialize('json',result)
                result_objs=json.loads(result_json)
                return render(request,'ModifyAttendanceList2.html',{'results':result_objs})
        instance = Attendance.objects.get(pk=pk)
        form = ModifyAttendanceSelectedForm(instance=instance)
        return render(request,'ModifyAttendanceSelected.html',{'form':form})
    return HttpResponse("<script>window.location.href = '../../Home';alert('Not Verified');</script>")

def raw_to_result(raw):
    result = {}
    total = 0
    for ele in raw:
        if ele['fields']['Subject_Code'] in result:
            if ele['fields']['Enrollment'] in result[ele['fields']['Subject_Code']]:
                if ele['fields']['Status']=='P':
                    result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['P']+=1
                    total += 1
                elif ele['fields']['Status']=='A':
                    result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['A']+=1
                    total += 1

            else:
                result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]={}
                if ele['fields']['Status']=='P':
                    total = 1
                    result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['P']=1
                    result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['A']=0
                elif ele['fields']['Status']=='A':
                    total = 1
                    result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['P']=0
                    result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['A']=1

        else:
            result[ele['fields']['Subject_Code']]={}
            result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]={}
            if ele['fields']['Status']=='P':
                total = 1
                result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['P']=1
                result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['A']=0
            elif ele['fields']['Status']=='A':
                total = 1
                result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['P']=0
                result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['A']=1
    return result


def CheckAttendanceList(request):
    UserId = request.user
    User_account = user_account.objects.get(username=UserId)
    if User_account.is_teacher and not User_account.is_pending:
        if request.method == 'POST':
            form = CheckAttendanceForm(request.POST)
            if form.is_valid():
                section = form.cleaned_data.get('Section')
                From = form.cleaned_data.get('From')
                To = form.cleaned_data.get('To')
                raw = Attendance.objects.filter(Section=section,Date__range=[From,To])
                raw_json = serializers.serialize('json',raw)
                result = raw_to_result(json.loads(raw_json))
                return render(request,'CheckAttendanceResult.html',{'results':result})                   #call function to calculate attendance of each student from data

        form = CheckAttendanceForm()
        return render(request,'CheckAttendance.html',{'form':form})
    return HttpResponse("<script>window.location.href = '../../Home';alert('Not Verified');</script>")

def TakeAttendance(request):
    UserId = request.user
    User_account = user_account.objects.get(username=UserId)
    if User_account.is_teacher and not User_account.is_pending:
        if request.method == 'POST':
            form = TakeAttendanceForm(request.POST)
            if form.is_valid():
                Sec = str(form.cleaned_data.get('Section').Section_Name)
                Class_Number = str(form.cleaned_data.get('Class').Class_Number)
                Camera_Id = str(form.cleaned_data.get('Class').Camera_Id)
                Subject_Code = str(form.cleaned_data.get('Subject').Subject_Code)
                return HttpResponse('Marking attendance of Students of Section <h4>'+Sec+'</h4> in Class <h4>'+Class_Number+' (Camera Id= '+Camera_Id+')</h4> for subject <h4>'+Subject_Code+'</h4>')

        form = TakeAttendanceForm()
        return render(request,'TakeAttendance.html',{'form':form})
    return HttpResponse("<script>window.location.href = '../../Home';alert('Not Verified');</script>")
