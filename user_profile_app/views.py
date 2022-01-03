from random import randint

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from .models import ResetPasswordOtp
from .serializers import UserProfile


# Create your views here.
class UserProfileView(APIView):
    def put(self, request):
        if User.objects.filter(email=request.data['email']).exists():
            user = User.objects.get(email=request.data['email'])
            serializerUser = UserProfile(user, data=request.data)
            if serializerUser.is_valid():
                serializerUser.save()
                return Response(
                    {"status": True, "msg": "Profile Successfully Updated", "data": serializerUser.data},
                    status=status.HTTP_200_OK
                )
            return Response(serializerUser.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": False, "msg": "User with email not found"})


class EmailVerify(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data["email"]
        userObj = User.objects.filter(email=email)

        if userObj.count() > 0:
            user = userObj.all()
            print(user[0].email)

            def otp_generator(num):
                range_start = 10 ** (num - 1)
                range_end = (10 ** num) - 1
                return randint(range_start, range_end)

            otp = otp_generator(6)
            user_id = user[0].id

            otp_obj = ResetPasswordOtp.objects.create(
                user_id=user_id,
                otp=otp,
            )
            otp_obj.save()
            subject = "Please Confirm Your Account"
            message = "Your 6 Digit Verification Pin: {}".format(otp)
            email_from = user[0].email
            returnecipient_list = [
                str(user[0].email),
            ]
            send_mail(subject, message, email_from, returnecipient_list)
            return Response(
                {
                    "status": True,
                    "msg": "OTP has been sent on your registered email id. Please check your email.",
                }
            )
        else:
            return Response(
                {
                    "status": False,
                    "msg": "Email does not exists. Please Try Again.",
                }
            )


class VerifyOtp(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data["email"]
        userObj = User.objects.filter(email=email)
        otp = int(request.data["otp"])
        if userObj.count() > 0:
            try:
                otpObj = ResetPasswordOtp.objects.get(otp=otp, user_id=userObj[0].id)
                if otp == otpObj.otp:
                    # id = otpObj.id
                    # print(id)
                    # a = OtpModel.objects.get(id=id).delete()
                    # print("444444444444", a)
                    return Response(
                        {
                            "status": True,
                            "msg": "OTP Verification Successfull.",
                        }
                    )
            except ResetPasswordOtp.DoesNotExist:
                return Response(
                    {
                        "status": False,
                        "msg": "OTP Verification Faild.",
                    }
                )
        else:
            return Response(
                {
                    "status": False,
                    "msg": "Invalid OTP. Please Try Again.",
                }
            )


class ResetPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data["email"]
        new_password = request.data["new_password"]
        confirm_password = request.data["confirm_password"]
        otp = int(request.data["otp"])
        userObj = User.objects.filter(email=email)

        otpObj = ResetPasswordOtp.objects.filter(otp=otp, user_id=userObj[0].id)
        if userObj.count() > 0 and otpObj.count() > 0:

            if userObj[0].id == otpObj[0].user_id:
                if new_password == confirm_password:
                    """make_password function converts a
                    plain-text password into a hash code."""
                    enc_pw = make_password(new_password)
                    psw = User.objects.get(id=userObj[0].id)
                    psw.password = enc_pw
                    psw.save()
                    otp_id = ResetPasswordOtp.objects.get(id=otpObj[0].id)
                    print(otp_id)
                    otp_id.delete()
                    return Response(
                        {
                            "status": True,
                            "msg": "New Password Set Successfull.",
                        }
                    )
                else:
                    return Response(
                        {
                            "status": False,
                            "msg": "New Password And Confirm Password Are Not Match",
                        }
                    )
        else:
            return Response(
                {
                    "status": False,
                    "msg": "Enter values not correct. Please Try Again.",
                }
            )
