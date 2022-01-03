from rest_framework import serializers

from .models import TestType


class TesttypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestType
        fields = [
            'id',
            'disease_name'
        ]
