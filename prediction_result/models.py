from django.db import models
from django.contrib.auth.models import User

def name_prediction_file(instance, filename):
    return '/'.join(['prediction_image', "", filename])


# Create your models here.
class PredictionResult(models.Model):
    class Meta:
        db_table="prediction_result"

    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    prediction_image=models.ImageField(upload_to=name_prediction_file)
    result_detail=models.TextField(null=True)
    result_length=models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
