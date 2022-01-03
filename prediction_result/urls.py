from django.urls import path, include
from .views import PredictionResultView
app_name = 'prediction_result'
urlpatterns = [
    path("create/", PredictionResultView.as_view(), name='create'),

]