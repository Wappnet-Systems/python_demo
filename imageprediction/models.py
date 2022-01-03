import datetime
import secrets

from django.contrib.auth.models import User
from django.db import models

from medical_iot.settings import UPLOAD_FOLDER
from patients.models import Patient
from testtype.models import TestType


# Create your models here.
class SampleData(models.Model):
    class Meta:
        db_table = "sample_data"

    AUTOSCOPE = 'autoscope'
    ACEIT = 'ace_it'
    mode_selection = ((AUTOSCOPE, 'autoscope'), (ACEIT, 'ace_it'))

    mode = models.CharField(choices=mode_selection, max_length=10, default=ACEIT)
    result = models.CharField(max_length=50, null=True)
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.patient_id.patient_full_name)

    def operator(self):
        return self.user_id.first_name + ' ' + self.user_id.last_name

    def patient(self):
        return self.patient_id.patient_full_name

    def testdetail(self):
        date_time_obj = datetime.datetime.strptime(str(self.created_at).split('+')[0], '%Y-%m-%d %H:%M:%S.%f')
        date = date_time_obj.date()
        time = datetime.datetime.strptime(str(date_time_obj.time()).split('.')[0][0:5], "%H:%M")
        time = time.strftime("%I:%M %p")
        return {
            'Date_of_test_done': date,
            'Time_of_test_done': time,
            'result': self.result,
            'mode': self.mode
        }

    def calage(self, date):
        today = date.today()
        age = today.year - date.year - ((today.month, today.day) <
                                        (date.month, date.day))
        return age

    def record(self):
        return {
            'patient_id': self.patient_id.id,
            'patient_name': self.patient_id.patient_full_name,
            'patient_age': self.calage(self.patient_id.patient_dob),
            'patient_location': self.patient_id.patient_location,
            'patient_gender': self.patient_id.patient_gender,
        }


class ImageData(models.Model):
    class Meta:
        db_table = 'image_table'

    def fileunique(self, filename):
        file, extension = secrets.token_hex(10)[1::3], filename.split('.')[1]
        filename = "{}-{}.{}".format(file, str(datetime.datetime.now()).split(' ')[0][5:10], extension)
        return '/'.join([UPLOAD_FOLDER, filename])

    image_name = models.ImageField(upload_to=fileunique)
    result_length = models.IntegerField()
    result = models.CharField(max_length=50)
    sample_data_id = models.ForeignKey(SampleData, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def img(self):
        return "%s" % (str(self.image_name)[57:])

    def patient(self):
        return self.sample_data_id.patient_id.patient_full_name
