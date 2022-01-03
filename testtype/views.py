from django.shortcuts import render
from rest_framework.decorators import APIView
from .models import TestType
from .serializer import TesttypeSerializer
from rest_framework.response import Response


# Create your views here.
class Testtype(APIView):
    def get(self, request):
        disease = TestType.objects.all().filter(status='enabled')
        serializer_class = TesttypeSerializer(disease, many=True)
        return Response(serializer_class.data)
