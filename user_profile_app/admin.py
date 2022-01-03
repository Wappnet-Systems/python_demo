from django.contrib import admin

from .models import ResetPasswordOtp


# Register your models here.
class otpDetail(admin.ModelAdmin):
    list_display = ('user', 'otp')


admin.site.register(ResetPasswordOtp, otpDetail)
