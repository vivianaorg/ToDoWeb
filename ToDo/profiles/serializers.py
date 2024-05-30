from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token


class ProfileCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["username", "password", "email", "bio"]

    def validate_email(self, value):
        existing_email = Profile.objects.filter(email=value).exists()
        if existing_email:
            raise serializers.ValidationError(
                "Ya existe un usuario con este correo electrónico."
            )
        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        user = super(ProfileCreationSerializer, self).create(validated_data)
        if user:
            return {"success": True, "message": "Usuario registrado exitosamente"}
        else:
            return {"success": False, "message": "Error al registrar usuario"}


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "username", "email", "bio"]
        read_only_fields = ["id"]