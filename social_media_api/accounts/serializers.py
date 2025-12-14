from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

from accounts.models import CustomUser


# Serializer for User Registration
class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    # MANDATORY: Defines the 'password' field specifically as CharField
    # 'write_only=True' ensures it's accepted on input but never returned on output.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        # 'password' must be included here to be accepted in the POST request
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'bio')

    # Custom create method to properly hash and save the password
    def create(self, validated_data):
        # The CustomUser manager handles create_user, hashing the password.
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', None)
        )
        return user

# Serializer for User Login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        data['user'] = user
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        data['token'] = token.key
        return data

# Serializer for viewing and updating user profile
class CustomUserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture',
            'date_joined', 'followers_count', 'following_count'
        )
        read_only_fields = ('username', 'email', 'date_joined', 'followers_count', 'following_count')

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']



# class CustomUserRegistrationSerializer(serializers.ModelSerializer):
#     # This line MUST be present.
#     password = serializers.CharField(write_only=True) 

#     class Meta:
#         model = CustomUser
#         # 'password' must be included in fields
#         fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'bio')

#     def create(self, validated_data):
#         # We access the CustomUser model directly here
#         user = CustomUser.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data.get('email', ''),
#             password=validated_data['password'], # Accessing the validated, unhashed password
#             first_name=validated_data.get('first_name', ''),
#             last_name=validated_data.get('last_name', ''),
#             bio=validated_data.get('bio', None)
#         )
#         return user

    
# class CustomUserProfileSerializer(serializers.ModelSerializer):
#     followers_count = serializers.SerializerMethodField()
#     following_count = serializers.SerializerMethodField()

#     class Meta:
#         model =CustomUser
#         fields = (
#             'id', 'username', 'email', 'first_name', 'last_name','bio', 'prfile_picture',
#             'followers_count', 'following_count'
#         )
#         read_only_fields = ('username', 'email', 'followers_count', 'following_count')

#         def get_followers_count(self, obj):
#             return obj.followers.count()
        
#         def get_following_count(self, obj):
#             return obj.following.count()#'following' is the related_name