from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import AttendanceSerializer
from account.models import Student,user_account,Teacher
from account.api.serializer import StudentProfileSerializer
from attendance.models import Attendance
from section.models import Class
import cmake
import cv2
import face_recognition
import shutil,os
import pickle
# Create your views here.

class StudentAttendanceList(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = Attendance.objects.filter(Enrollment=request.data.get('enrollment'),Section=request.data.get('section'))
            result = AttendanceSerializer(data, many=True)
            return Response(result.data, status=200)
        except Exception as e:
            return Response(e,status=400)
    def get(self,request,username):
        try:
            profile = Student.objects.get(Enrollment=username)
            if profile is not None:
                section_name = profile.Section
                data = Attendance.objects.filter(Enrollment=profile, Section=section_name)
                result = AttendanceSerializer(data, many=True)
                return Response(result.data, status=200)
            else:
                return Response('some error occur', status=400)
        except Exception as E:
            return Response(E.__str__(), status=404)


class ModifyAttendanceList(APIView):
    def put(self, request, *args, **kwargs):
        try:
            data = Attendance.objects.get(Enrollment=request.data.get('Enrollment'),Section=request.data.get('Section'),Subject_Code=request.data.get('Subject_Code'),Date=request.data.get('Date'))
            result = AttendanceSerializer(data,request.data)
            if result.is_valid():
                result.save()
                return Response('Data updated',status=200)
            return Response('Data is not updated', status=400)
        except Exception as E:
            return Response(E.__str__(),status=400)
    def get(self,request,date,section,subject_code):
        try:
            data = Attendance.objects.filter(Subject_Code=subject_code,Section=section,Date=date)
            result=AttendanceSerializer(data, many=True)
            return Response(result.data,status=200)
        except Exception as E:
            return Response(E.__str__(),status=400)

class CheckAttendance(APIView):
    def get(self,request,section,subject_code,from_date,to_date):
        try:
            data = Attendance.objects.filter(Subject_Code=subject_code, Section=section, Date__range=[from_date,to_date])
            raw_result = AttendanceSerializer(data,many=True)
            result = self.raw_to_result(raw_result.data)
            return Response(result, status=200)
        except Exception as E:
            return Response(E.__str__(), status=500)

    def raw_to_result(self,raw):
        result = {}
        total = 0
        for ele in raw:
            if ele['Subject_Code'] in result:
                if ele['Enrollment'] in result[ele['Subject_Code']]:
                    if ele['Status'] == 'P':
                        result[ele['Subject_Code']][ele['Enrollment']]['P'] += 1
                        total += 1
                    elif ele['Status'] == 'A':
                        result[ele['Subject_Code']][ele['Enrollment']]['A'] += 1
                        total += 1

                else:
                    result[ele['Subject_Code']][ele['Enrollment']] = {}
                    if ele['Status'] == 'P':
                        total = 1
                        result[ele['Subject_Code']][ele['Enrollment']]['P'] = 1
                        result[ele['Subject_Code']][ele['Enrollment']]['A'] = 0
                    elif ele['Status'] == 'A':
                        total = 1
                        result[ele['Subject_Code']][ele['Enrollment']]['P'] = 0
                        result[ele['Subject_Code']][ele['Enrollment']]['A'] = 1

            else:
                result[ele['Subject_Code']] = {}
                result[ele['Subject_Code']][ele['Enrollment']] = {}
                if ele['Status'] == 'P':
                    total = 1
                    result[ele['Subject_Code']][ele['Enrollment']]['P'] = 1
                    result[ele['Subject_Code']][ele['Enrollment']]['A'] = 0
                elif ele['Status'] == 'A':
                    total = 1
                    result[ele['Subject_Code']][ele['Enrollment']]['P'] = 0
                    result[ele['Subject_Code']][ele['Enrollment']]['A'] = 1
        return result

class TakeAttendance(APIView):
    def get(self,request,section,subject_code,class_id):
        try:
            class_info = Class.objects.get(Class_Number=class_id)
            camera_id = class_info.Camera_Id
            Enrollment_List = self.Enrollment_List_Maker(section)
            data_list = self.MarkAttendance(Enrollment_List,camera_id)
            return Response(data_list)
        except Exception as E:
            return Response(E.__str__(), status=500)

    def Enrollment_List_Maker(self,section):
        Student_List = Student.objects.filter(Section=section)
        Student_Info = StudentProfileSerializer(Student_List, many=True)
        data = []
        for row in Student_Info.data:
            data.append(row['Enrollment'])
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
        result['total_Face']=len(facedata_list)
        for Enrollment in Enrollment_List:
            facedata_old_str = self.fetch_face_data(Enrollment)
            if facedata_old_str==0:
                result[Enrollment]='Face Data Not Found'
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
        return result
    
    def fetch_face_data(self,Enrollment):
        result = 0
        try:
            data = FaceData.objects.get(Enrollment=Enrollment)
            result = data.Face_Data
        except:
            result = 0
        return result
        
class LoadFace(APIView):
    def post(self, request, *args, **kwargs):
        try:
            files = os.scandir('./ImageData/to_add/')
            lst=[]
            for file in files:
                lst.append(str(file.name))
            for file in lst:
                img = face_recognition.load_image_file('./ImageData/to_add/'+file)
                img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                facedata = face_recognition.face_encodings(img)[0]
                ins = FaceData()
                ins.Enrollment = Student.objects.get(Enrollment = file[:file.find('.')])
                ins.Face_Data = pickle.dumps(facedata)
                ins.save()
                shutil.move('./ImageData/to_add/'+file,'./ImageData/all/')
                
            return Response(lst)
        except Exception as e:
            return Response(e.__str__())