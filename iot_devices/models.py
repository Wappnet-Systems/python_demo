from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class IotDevice(models.Model):
    ON = 'on'
    OFF = 'off'

    device_status_option = ((ON, 'on'), (OFF, 'off'))

    class Meta:
        db_table = "iot_devices"

    device_id = models.IntegerField(null=True)
    iot_device_name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, null=True)
    device_status = models.CharField(max_length=5, default=OFF, choices=device_status_option)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.device_id)


class operatorDevices(models.Model):
    class Meta:
        db_table = 'operator_device'

    device_id = models.OneToOneField(IotDevice, on_delete=models.CASCADE, related_name='devices')
    operator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.device_id.iot_device_name)
    
    def operator(self):
        return self.operator_id.first_name + ' ' + self.operator_id.last_name

    def device(self):
        device = [
            {
                'device_id': self.device_id.device_id,
                'iot_device_name': self.device_id.iot_device_name,
                'device_status': self.device_id.device_status,
                'type': self.device_id.type
            }
        ]
        return device
