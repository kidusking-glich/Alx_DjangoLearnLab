from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import CustomUserRegistrationSerializer, CustomUserProfileSerializer
from .models import CustomUser

# Create your views here.

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        token, created = Token.objects.get_or_create(user = user)

        return Response({
            'user': CustomUserProfileSerializer(user).data,
            'token': token.key
        }, status=201)
    

class LoginUserView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': CustomUserProfileSerializer(user).data,
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Enforce that users can only view/edit their own profile
        return self.request.user