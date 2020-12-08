from rest_framework import serializers
from django.contrib.auth import authenticate
from account.models import Student,Teacher,user_account

class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)
        data = False
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        if user.is_student:
            try:
                profile = Student.objects.get(Enrollment=user.username)
                if profile is not None:
                    data=True
            except:
                pass
        elif user.is_teacher:
            try:
                profile = Teacher.objects.get(Id=user.username)
                if profile is not None:
                    data=True
            except:
                pass

        return {
            'username':user.username,
            'is_student':user.is_student,
            'is_teacher':user.is_teacher,
            'is_pending':user.is_pending,
            'Registered':data
        }

class AccountSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=user_account
        fields = ['username','password','password2','is_student','is_teacher']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def save(self):
        Account=    user_account(username=self.validated_data['username'],is_student=self.validated_data['is_student'],is_teacher=self.validated_data['is_teacher'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password':'password must match'})
        Account.set_password(password)
        Account.save()
        return Account

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields = ['Name','Mobile','Email','Year','Semester','Department','Enrollment','Section']
    def create(self,validated_data):
        return Student.objects.create(**validated_data)
    

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields = ['Name','Mobile','Email','Id']
    def create(self,validated_data):
        return Teacher.objects.create(**validated_data)
