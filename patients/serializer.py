from rest_framework import serializers

from .models import Patientoperator, Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id',
            'patient_full_name',
            'patient_dob',
            'patient_email',
            'patient_contact'
        ]


class PatientoperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patientoperator
        fields = [
            'id',
            'operator_id',
            'patient_id',
            'status',
            'patient'
        ]
