import datetime

from django.http import Http404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import APIView
from rest_framework.response import Response

from .models import Patient, Patientoperator
from .serializer import PatientoperatorSerializer, PatientSerializer


# Create your views here.
class OpertorPatient(APIView):
    def get(self, request):
        operator_token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        operator_id = Token.objects.get(key=operator_token).user_id
        patients = Patientoperator.objects.filter(operator_id=operator_id).exclude(status='removed')
        serializer_class = PatientoperatorSerializer(patients, many=True)
        return Response(serializer_class.data)


class PatientDetail(APIView):
    def get_patient(self, pk):
        return Patient.objects.get(id=pk)

    def get(self, request):
        try:
            if Patient.objects.filter(patient_email=request.data['patient_email']).exists():
                patient_id = Patient.objects.filter(patient_email=request.data['patient_email'])[0].id
                patient = self.get_patient(patient_id)
                serializer_class_patient = PatientSerializer(patient)
                return Response(serializer_class_patient.data)
            else:
                return Response({"status": False, "msg": "Patient detail not found"},
                                status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Http404


class UpdatePatient(APIView):
    def get_patient(self, pk):
        return Patient.objects.get(id=pk)

    def delete(self, request):
        try:
            if Patient.objects.filter(patient_email=request.data['patient_email']).exists():
                patient_id = Patient.objects.filter(patient_email=request.data['patient_email'])[0].id
                patient = self.get_patient(patient_id)
                patient.delete()
                return Response({"status": True, "msg": "Patient Successfully Deleted"})
            else:
                return Response({"status": False, "msg": "Patient not found"}, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"status": False, "msg": "Patient not found"}, status=status.HTTP_200_OK)

    def put(self, request):
        try:
            if Patient.objects.filter(patient_email=request.data['patient_email']).exists():
                patient_id = Patient.objects.filter(patient_email=request.data['patient_email'])[0].id
                patient = self.get_patient(patient_id)
                patient_date = request.data['patient_dob'].split('/')[::-1]
                patient_dob = datetime.date(int(patient_date[0]), int(patient_date[1]), int(patient_date[2]))
                request_patient_dob = {'patient_dob': patient_dob}

                request.data._mutable = True
                request.data.pop('patient_dob')
                request.data.update(request_patient_dob)
                serializer_class_patient = PatientSerializer(patient, data=request.data)

                if serializer_class_patient.is_valid():
                    serializer_class_patient.save()
                    return Response({"status": True, "msg": "Successfully updated Patient"},
                                    status=status.HTTP_200_OK)
                else:
                    return Response(serializer_class_patient.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"status": False, "msg": "Patient not found"}, status=status.HTTP_200_OK)
        except:
            return Response({"status": False, "msg": "Patient not found"}, status=status.HTTP_200_OK)


class InsertPatients(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        serializer_class = PatientSerializer(patients, many=True)
        return Response(serializer_class.data)

    def post(self, request):

        my_token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        validation = Patient.objects.filter(patient_email=request.data['patient_email']).exists()
        if validation == False:
            patient_date = request.data['patient_dob'].split('/')[::-1]
            patient_dob = datetime.date(int(patient_date[0]), int(patient_date[1]), int(patient_date[2]))
            request_patient_dob = {'patient_dob': patient_dob}

            request.data._mutable = True
            request.data.pop('patient_dob')
            request.data.update(request_patient_dob)
            serializer_class_patient = PatientSerializer(data=request.data)

            if serializer_class_patient.is_valid():
                serializer_class_patient.save()
                patient_id = {'patient_id': Patient.objects.filter(patient_email=request.data['patient_email'])[0].id}
                operator_id = {'operator_id': Token.objects.get(key=my_token).user_id}

                request.data.update(operator_id)
                request.data.update(patient_id)
                request.data.update({"status": "assign"})
                serializer_class_operatorpatient = PatientoperatorSerializer(data=request.data)

                if serializer_class_operatorpatient.is_valid():
                    serializer_class_operatorpatient.save()
                    return Response({"status": True, "msg": "Successfully inserted Patient"}, status=status.HTTP_200_OK)

            return Response(serializer_class_patient.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": False, "msg": "Patient email is already register"}, status=status.HTTP_200_OK)
