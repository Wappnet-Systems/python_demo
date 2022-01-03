from django.urls import path
from rest_framework import routers

from . import views

app_name = "user_profile_app"

router = routers.DefaultRouter()

urlpatterns = [
    path('user/', views.UserProfileView.as_view()),
    path("forgot_password/", views.EmailVerify.as_view()),
    path("verifyotp/", views.VerifyOtp.as_view()),
    path("reset_password/", views.ResetPassword.as_view()),
]
