from django.shortcuts import render
from rest_auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

class CustomLoginView(LoginView):
    @csrf_exempt
    def get_response(self):
        orginal_response = super().get_response()
        return orginal_response
        mydata = {"message": "some message", "status": "success"}
        orginal_response.data.update(mydata)
        return orginal_response
