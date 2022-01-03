from django.contrib import admin
from django.contrib import messages
from .models import Patient, Patientoperator


# Register your models here.

class PatientDetail(admin.ModelAdmin):
    list_display = (
        'patient_full_name', 'patient_dob', 'patient_email', 'patient_contact', 'patient_location', 'patient_gender')
    search_fields = ('patient_full_name', 'patient_email', 'patient_contact', 'patient_location')
    list_filter = ('patient_gender',)


class PatientoperatorDetail(admin.ModelAdmin):
    list_display = ('patientname', 'operator', 'status')
    search_fields = ('patient_id__patient_full_name', 'operator_id__first_name', 'operator_id__last_name')
    list_editable = ('status',)
    list_filter = ('status',)

    def response_add(self, request, obj, post_url_continue=None):
        msg = "Patient {} is assign sucessfully to operator".format(obj.patient_id)
        self.message_user(request, msg, level=messages.SUCCESS)
        return self.response_post_save_add(request, obj)

    def response_change(self, request, obj):
        msg = "sucessfully updated".format(obj.patient_id)
        self.message_user(request, msg, level=messages.SUCCESS)
        return self.response_post_save_add(request, obj)

    def save_model(self, request, obj, form, change):
        def updateStatus(patient_id):
            Patientoperator.objects.filter(patient_id=patient_id).update(status='removed')

        updateStatus(obj.patient_id)
        super(PatientoperatorDetail, self).save_model(request, obj, form, change)


admin.site.register(Patient, PatientDetail)
admin.site.register(Patientoperator, PatientoperatorDetail)
