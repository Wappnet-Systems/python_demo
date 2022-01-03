from rest_framework import serializers

from .models import SampleData, ImageData


class SampleDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleData
        fields = [
            'mode',
            'result',
            'test_type',
            'patient_id',
            'user_id',
        ]


class ImageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageData
        fields = [
            'image_name',
            'result_length',
            'result',
            'sample_data_id',
        ]


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleData
        fields = [
            'testdetail',
            'record'
        ]
