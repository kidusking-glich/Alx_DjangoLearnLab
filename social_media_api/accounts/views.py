from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import CustomUserRegistrationSerializer, CustomUserProfileSerializer, LoginSerializer, UserFollowSerializer
from .models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework import views, permissions, status

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
        }, status=201, headers=self.get_success_headers(serializer.data))
    

class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = serializer.validated_data['token']

        # Get profile data for the response
        user_serializer = CustomUserProfileSerializer(user)

        return Response({
            'token': token,
            'user': user_serializer.data,
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Enforce that users can only view/edit their own profile
        return self.request.user

class TokenRetrievalView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        return Response({'token': token.key})
    

class FollowAPIView(views.APIView):
    """
    Endpoint to explicitly FOLLOW a user. (POST request)
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, pk=user_id)
        current_user = request.user

        if target_user == current_user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if current_user.user_following.filter(pk=target_user.pk).exists():
            return Response(
                {"detail": "You are already following this user."},
                status=status.HTTP_409_CONFLICT # Conflict status for already followed
            )

        current_user.user_following.add(target_user)
        
        return Response(
            {"detail": f"Successfully followed user {target_user.username}"},
            status=status.HTTP_201_CREATED
        )

class UnfollowAPIView(views.APIView):
    """
    Endpoint to explicitly UNFOLLOW a user. (DELETE request)
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id):
        target_user = get_object_or_404(CustomUser, pk=user_id)
        current_user = request.user

        if target_user == current_user:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if following before attempting to remove
        if not current_user.user_following.filter(pk=target_user.pk).exists():
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_404_NOT_FOUND # Not found, as the relationship doesn't exist
            )

        current_user.user_following.remove(target_user)
        
        return Response(
            {"detail": f"Successfully unfollowed user {target_user.username}"},
            status=status.HTTP_204_NO_CONTENT # Standard status for successful deletion
        )