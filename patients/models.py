import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validate_email(email):
    email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if (re.search(email_regex, email)):
        return True
    else:
        raise ValidationError("Please enter a valid email address.")


def validatecontact(contact):
    contact_regex = '[0-9]{10,12}'
    if (re.search(contact_regex, contact)):
        return True
    else:
        raise ValidationError('Please enter a valid contact number.')


# Create your models here.

class Patient(models.Model):
    class Meta:
        db_table = 'patients_table'

    MALE = 'male'
    FEMALE = 'female'
    select_gender = ((MALE, 'male'), (FEMALE, 'female'))

    patient_full_name = models.CharField(max_length=50)
    patient_dob = models.DateField()
    patient_email = models.EmailField(max_length=150, validators=[validate_email], unique=True)
    patient_contact = models.CharField(max_length=12, validators=[validatecontact])
    patient_location = models.CharField(max_length=50)
    patient_gender = models.CharField(max_length=10, choices=select_gender)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.patient_full_name)


class Patientoperator(models.Model):
    PENDING = 'pending'
    ASSIGN = 'assign'
    REMOVED = 'removed'

    patient_status_option = ((PENDING, 'pending'), (ASSIGN, 'assign'), (REMOVED, 'removed'))

    class Meta:
        db_table = 'patient_operator'

    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    operator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=patient_status_option, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}  {}  {}".format(self.patient_id, self.operator_id, self.status)

    def operator(self):
        return self.operator_id.first_name + ' ' + self.operator_id.last_name

    def patientname(self):
        return self.patient_id.patient_full_name

    def patient(self):
        patient = [
            {
                'patient_full_name': self.patient_id.patient_full_name,
                'patient_dob': self.patient_id.patient_dob,
                'patient_email': self.patient_id.patient_email,
                'patient_contact': self.patient_id.patient_contact,
                'status': self.status
            }

        ]
        return patient
