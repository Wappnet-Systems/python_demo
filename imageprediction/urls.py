from django.urls import path

from .views import ImagePredection

app_name = 'imageprediction'
urlpatterns = [
    path('predict/', ImagePredection.as_view(), name='predict')
]
