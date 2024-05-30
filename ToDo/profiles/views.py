from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import (
    ProfileCreationSerializer,
    ProfileSerializer,
    CustomTokenObtainPairSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProfileCreationView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileCreationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        if response_data.get("success"):
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]