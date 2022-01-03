from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import PredictionResult
from .serializer import PredictionResultSerializer
from rest_framework import status
# Create your views here.
class PredictionResultView(APIView):
    queryset = PredictionResult.objects.all()
    serializer_class=PredictionResultSerializer

    def post(self,request):
        file = request.data['prediction_image']
        image = PredictionResult.objects.create(prediction_image=file)
        return Response({"status": True, "msg": "Successfully Created"}, status=status.HTTP_200_OK)
