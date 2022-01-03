from django import forms
from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html

from .models import IotDevice, operatorDevices


# Register your models here.
class DeviceForm(forms.ModelForm):
    class Meta:
        model = IotDevice
        exclude = ['device_id', 'device_status']


class DeviceDetail(admin.ModelAdmin):
    form = DeviceForm
    list_display = ('device_id', 'iot_device_name', 'type', 'device_status', 'Qrcode')
    search_fields = ('device_id', 'iot_device_name', 'type')
    list_filter = ('device_status',)

    def response_add(self, request, obj, post_url_continue=None):
        msg = "Device {} is added sucessfully".format(obj.iot_device_name)
        self.message_user(request, msg, level=messages.SUCCESS)
        return self.response_post_save_add(request, obj)

    def response_change(self, request, obj):
        msg = "Device {} sucessfully updated".format(obj.iot_device_name)
        self.message_user(request, msg, level=messages.SUCCESS)
        return self.response_post_save_add(request, obj)

    def save_model(self, request, obj, form, change):
        def updatedevice():
            Add_constant = 10000
            id_last = IotDevice.objects.last().id
            device_id = Add_constant + id_last
            deviceObj = IotDevice.objects.get(id=id_last)
            deviceObj.device_id = device_id
            deviceObj.save()

        super(DeviceDetail, self).save_model(request, obj, form, change)
        updatedevice()

    def Qrcode(self, obj):
        return format_html(
            '<a href="https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl={}&choe=UTF-8" target="_blank" class="default">view</a>'.format(
                obj.device_id))


class OperatordeviceDetail(admin.ModelAdmin):
    list_display = ['device_id', 'operator']
    search_fields = ('device_id__device_id', 'operator_id__first_name', 'operator_id__last_name')

    def response_add(self, request, obj, post_url_continue=None):
        msg = "Device {} is assign sucessfully to operator".format(obj.device_id)
        self.message_user(request, msg, level=messages.SUCCESS)
        return self.response_post_save_add(request, obj)

    def response_change(self, request, obj):
        msg = "sucessfully updated".format(obj.device_id)
        self.message_user(request, msg, level=messages.SUCCESS)
        return self.response_post_save_add(request, obj)
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(IotDevice, DeviceDetail)
admin.site.register(operatorDevices, OperatordeviceDetail)
