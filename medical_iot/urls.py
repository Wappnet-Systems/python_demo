"""medical_iot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Medical IOT"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path("user_profile_app/", include("user_profile_app.urls", namespace="user_profile_app")),
    path('iot_devices/', include('iot_devices.urls', namespace="iot_devices")),
    path('patients/', include('patients.urls', namespace='patients')),
    path('imageprediction/', include('imageprediction.urls', namespace='imageprediction')),
    path('testtype/', include('testtype.urls', namespace='testtype'))
    # path('custom_auth/',include('custom_auth.urls')),
]
