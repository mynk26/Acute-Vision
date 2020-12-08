from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserLoginSerializer,TeacherProfileSerializer,StudentProfileSerializer,AccountSerializer
from account.models import Student,user_account,Teacher
# Create your views here.
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serialize = UserLoginSerializer(data=request.data)
            result = serialize.validate(request.data)
            return Response(result)
        except Exception as E:
            return Response(E.__str__(), status=500)

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serialize = AccountSerializer(data=request.data)
            data={}
            if serialize.is_valid():
                try:
                    result = serialize.save()
                except:
                    return Response("can't save the object",status=400)
                data['response']='successfully register a new user.'
                data['username']=result.username
                data['is_student']=result.is_student
                data['is_teacher']=result.is_teacher
                data['registered']=False
            else:
                return Response('Validation Error',status=400)
            return Response(data,status=201)
        except Exception as E:
            return Response(E.__str__(), status=500)

class StudentProfileView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serialize = StudentProfileSerializer(data=request.data)
            data={}
            if serialize.is_valid():
                result = serialize.validate(request.data)
                serialize.save()
                instance = user_account.objects.get(username=request.data.get('Enrollment'))
                data['username']=instance.username
                data['is_student']=instance.is_student
                data['is_teacher']=instance.is_teacher
                data['is_pending']=instance.is_pending
            else:
                return Response('Some Error Occur',status=400)
            return Response(data)
        except Exception as E:
            return Response(E.__str__(), status=500)
    def put(self,request,*args,**kwargs):
        try:
            profile = Student.objects.get(Enrollment=request.data.get('Enrollment'))
            serialize = StudentProfileSerializer(profile,data=request.data)
            if serialize.is_valid():
                serialize.save(Department=profile.Department,Semester=profile.Semester,Year=profile.Year,Section=profile.Section)
                return Response('Profile Successfully updated',status=200)
            else:
                return Response(serializer.errors,status=400)
        except Exception as E:
            return Response(E.__str__(), status=500)
    def get(self,request,username):
        try:
            profile = Student.objects.get(Enrollment=username)
        except Exception as E:
            return Response(E.__str__(), status=404)
        if profile is not None:
            data=StudentProfileSerializer(profile)
            return Response(data.data)
        else:
            return Response('some error occur',status=400)



class TeacherProfileView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serialize = TeacherProfileSerializer(data=request.data)
            data={}
            if serialize.is_valid():
                serialize.validate(request.data)
                serialize.save()
                instance = user_account.objects.get(username=request.data.get('Id'))
                data['username'] = instance.username
                data['is_student'] = instance.is_student
                data['is_teacher'] = instance.is_teacher
                data['is_pending'] = instance.is_pending
            else:
                return Response('Some Error Occur',status=400)
            return Response(data)
        except Exception as E:
            return Response(E.__str__(), status=500)
    def put(self,request,*args,**kwargs):
        try:
            profile = Teacher.objects.get(Id=request.data.get('Id'))
            serialize = TeacherProfileSerializer(profile,data=request.data)
            if serialize.is_valid():
                serialize.save()
                return Response('Profile Successfully updated',status=200)
            else:
                return Response(serializer.errors)
        except Exception as E:
            return Response(E.__str__(), status=500)

    def get(self,request,id):
        try:
            profile = Teacher.objects.get(Id=id)
        except:
            return Response('Profile not found', status=404)
        if profile is not None:
            data=TeacherProfileSerializer(profile)
            return Response(data.data)
        else:
            return Response('some error occur',status=400)