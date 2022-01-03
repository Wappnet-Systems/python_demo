from django.urls import path
from .views import DeviceViewCreate, RemoveOperatordevice, Userdevices

app_name = 'iot_devices'

urlpatterns = [
    path("create/", DeviceViewCreate.as_view(), name='create'),
    path("removeoperatordevice/", RemoveOperatordevice.as_view(), name='removeoperatordevice'),
    path("user/devices/", Userdevices.as_view(), name='viewdevices'),

]
