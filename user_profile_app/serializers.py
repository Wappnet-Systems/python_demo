from django.contrib.auth.models import User
from rest_framework import serializers


class UserProfile(serializers.ModelSerializer):
    email = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            'username',
            "email"
        ]


class EmailVerification(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]
