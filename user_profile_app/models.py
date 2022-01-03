from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class ResetPasswordOtp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    generated_at = models.DateTimeField(auto_now_add=True)
