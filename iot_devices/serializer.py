from rest_framework import serializers

from .models import IotDevice, operatorDevices


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IotDevice
        fields = [
            'id',
            'device_id',
            'iot_device_name',
            'device_status',
            'type',
        ]


class DeviceoperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = operatorDevices
        fields = [
            'id',
            'operator_id',
            'device_id',
            'device'
        ]
