from rest_framework import serializers
from .models import PredictionResult
from rest_framework.fields import CurrentUserDefault
class PredictionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionResult
        fields=[
            'user_id','prediction_image','result_detail','result_length','created_at','updated_at'
        ]
    def save(self, **kwargs):
        user_id=CurrentUserDefault()
        prediction_image=self.validated_data['prediction_image']
