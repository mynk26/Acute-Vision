from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import SubjectSerializer
from time_table.models import Subject
# Create your views here.
class Subject_List(APIView):
    def get(self,request,department,semester):
        try:
            data = Subject.objects.filter(Department=department,Semester=semester)
            result = SubjectSerializer(data, many=True)
            return Response(result.data, status=200)
        except Exception as E:
            return Response(E, status=400)
