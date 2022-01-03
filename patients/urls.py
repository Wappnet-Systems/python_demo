from django.urls import path

from .views import InsertPatients, UpdatePatient, PatientDetail, OpertorPatient

app_name = 'patients'
urlpatterns = [
    path('patient/', InsertPatients.as_view(), name='patient'),
    path('patientope/', UpdatePatient.as_view(), name='patientope'),
    path('patientdetail/', PatientDetail.as_view(), name='patientdetail'),
    path("operatorpatients/", OpertorPatient.as_view(), name='operatorpatients')
]
