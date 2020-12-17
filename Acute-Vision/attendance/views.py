from django.http import HttpResponse
from django.core import serializers
from django.utils import timezone
import json
from django.shortcuts import render
from account.models import user_account,Student,FaceData
from section.models import Class,Section
from attendance.api.serializer import AttendanceSerializer
from time_table.models import Subject
from .models import Attendance
from django.conf import settings
import cmake
import cv2
import face_recognition
import shutil,os
import pickle
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
                Subject_Code = str(form.cleaned_data.get('Subject').Subject_Code)
                Subject_Code_ins = Subject.objects.get(Subject_Code=Subject_Code)
                date = timezone.now().date()
                Section_ins = Section.objects.get(Section_Name = Sec)
                data,length= FaceFunctions().get(Sec,Subject_Code,Class_Number)
                result = {}
                result['Total Faces'] = length
                result['A']=0
                result['P']=0
                for Enrollment,status in data.items():
                    E=Student.objects.get(Enrollment=Enrollment)
                    Status=''
                    if status == 'A':
                        result['A']+=1
                        Status='A'
                    elif status =='P':
                        result['P']+=1
                        Status='P'
                    else:
                        result['Data Not Found'] +=str(Enrollment)+' '
                        Status = 'A'
                    ins = Attendance.objects.create(Enrollment=E,Subject_Code=Subject_Code_ins,Section=Section_ins,Date=date,Status=Status)
                    try:
                        ins.save()
                    except Exception as e:
                        result[e.__str__()+' at:']=str(Enrollment)
                return HttpResponse(result.items())

        form = TakeAttendanceForm()
        return render(request,'TakeAttendance.html',{'form':form})
    return HttpResponse("<script>window.location.href = '../../Home';alert('Not Verified');</script>")


class FaceFunctions():
    def get(self,section,subject_code,class_id):
        try:
            class_info = Class.objects.get(Class_Number=class_id)
            camera_id = class_info.Camera_Id
            Enrollment_List = self.Enrollment_List_Maker(section)
            data_list = self.MarkAttendance(Enrollment_List,camera_id)
            return data_list
        except Exception as E:
            return E.__str__()

    def Enrollment_List_Maker(self,section):
        Student_List = Student.objects.filter(Section=section)
        data = []
        for row in Student_List:
            data.append(row.Enrollment)
        return data

    def MarkAttendance(self,Enrollment_List,Camera_Id):
        result={}
        cam = cv2.VideoCapture(0)                 # later we change it to camera id
        frame = cam.read()[1]
        cam.release()
        cv2.imwrite('temp.jpg',frame)
        img = face_recognition.load_image_file('temp.jpg')
        os.remove('temp.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        facedata_list = face_recognition.face_encodings(img) 
        length=len(facedata_list)
        for Enrollment in Enrollment_List:
            facedata_old_str = self.fetch_face_data(Enrollment)
            if facedata_old_str==0:
                result[Enrollment]=-1
                continue
            facedata_old = pickle.loads(facedata_old_str)
            count=0
            for facedata in facedata_list:
                if face_recognition.compare_faces([facedata,],facedata_old)[0]:
                    result[Enrollment]='P'
                    count=1
                    break
            if count==0:
                result[Enrollment] = 'A'
        return result,length
    def fetch_face_data(self,Enrollment):
        result = 0
        try:
            data = FaceData.objects.get(Enrollment=Student.objects.get(Enrollment=Enrollment))
            result = data.Face_Data
        except Exception as e:
            result = 0
            return e.__str__()
        return result