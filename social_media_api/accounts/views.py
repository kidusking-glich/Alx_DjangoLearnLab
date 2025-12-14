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
    Endpoint to follow or unfollow a user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # The user being followed/unfollowed
        target_user = get_object_or_404(CustomUser, pk=user_id)
        current_user = request.user

        if target_user == current_user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if already following
        if current_user.is_following(target_user):
            # If following, UNFOLLOW
            current_user.following.remove(target_user)
            action = 'unfollowed'
        else:
            # If not following, FOLLOW
            current_user.following.add(target_user)
            action = 'followed'
        
        return Response(
            {"detail": f"Successfully {action} user {target_user.username}", "user": UserFollowSerializer(target_user).data},
            status=status.HTTP_200_OK
        )
