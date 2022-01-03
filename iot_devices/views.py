from django.http import Http404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import APIView
from rest_framework.response import Response

from .models import IotDevice, operatorDevices
from .serializer import DeviceoperatorSerializer


# Create your views here.
class DeviceViewCreate(APIView):
    def validation(self, devId):
        if IotDevice.objects.filter(device_id=devId).exists():
            id = IotDevice.objects.filter(device_id=devId)[0].id
            validate = operatorDevices.objects.filter(device_id_id=id).exists()
            if validate == False:
                return IotDevice.objects.filter(device_id=devId)[0].id
            else:
                return None
        else:
            return False

    def get(self, request):
        device = operatorDevices.objects.all()
        serializer_class = DeviceoperatorSerializer(device, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        devid = self.validation(request.data['device_id'])
        if devid != False:
            if devid != None:
                my_token = request.META.get('HTTP_AUTHORIZATION').split()[1]
                operator_id = {"operator_id": Token.objects.get(key=my_token).user_id}
                device_id = {"device_id": IotDevice.objects.filter(device_id=request.data['device_id'])[0].id}
                request_user = operator_id
                request_device_id = device_id
                request.data._mutable = True
                request.data.update(request_user)
                request.data.update(request_device_id)
                serializer_class = DeviceoperatorSerializer(data=request.data)
                if serializer_class.is_valid():
                    IotDevice.objects.filter(id=devid).update(device_status='on')
                    serializer_class.save()
                    return Response({"status": True, "msg": "Successfully Created"}, status=status.HTTP_200_OK)
                return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"status": False, "msg": "Device is already assign to an operator"},
                                status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "msg": "Device detail not found"},
                            status=status.HTTP_200_OK)


class Userdevices(APIView):
    def get_object(self, pk):
        return operatorDevices.objects.filter(operator_id=pk)

    def get(self, request):
        my_token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        user_id = Token.objects.get(key=my_token).user_id
        device = self.get_object(user_id).select_related()
        serializer_class = DeviceoperatorSerializer(device, many=True)
        return Response(serializer_class.data)


class RemoveOperatordevice(APIView):
    def get_object(self, device_id, operator_id):
        try:
            return operatorDevices.objects.get(device_id=device_id, operator_id=operator_id)
        except operatorDevices.DoesNotExist:
            return None

    def delete(self, request):
        try:
            if IotDevice.objects.filter(device_id=request.data['device_id']).exists():
                device_id = IotDevice.objects.filter(device_id=request.data['device_id'])[0].id
                my_token = request.META.get('HTTP_AUTHORIZATION').split()[1]
                operator_id = Token.objects.get(key=my_token).user_id
                deviceoperator = self.get_object(device_id, operator_id)
                if deviceoperator != None:
                    IotDevice.objects.filter(id=device_id).update(device_status='off')
                    deviceoperator.delete()
                    return Response({"status": True, "msg": "Device operator successfully deleted"})
                else:
                    return Response({"status": False, "msg": "Operator with device not found"})
            else:
                return Response({"status": False, "msg": "Device not found"})
        except operatorDevices.DoesNotExist:
            return Response({"status": False, "msg": "Device Not Exist"})
