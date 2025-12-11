from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token


# class CustomUserRegistrationSerializer(serializers.ModelSerializer):
#     password =serializers.CharField(write_only=True)

#     class Meta:
#         model =CustomUser
#         fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'bio')

#     def create(self, validated_data):
#         # Retrieve the required 'password' field and hash it
#         password = validated_data.pop('password')

#         # Create the user using the remaining validated data
#         user = CustomUser.objects.create_user(
#             username= validated_data['username'],
#             email = validated_data.get('email', ''),
#             password=validated_data['password'],

#             # Ensure all field retrievals use brackets or .get()
#             first_name=validated_data.get('first_name', ''), 
#             last_name=validated_data.get('last_name', ''), 
#             bio=validated_data.get('bio', None)
#         )
#         return user 






# Serializer for User Registration
class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    # MANDATORY: Defines the 'password' field specifically as CharField
    # 'write_only=True' ensures it's accepted on input but never returned on output.
    password = serializers.CharField(write_only=True) 

    class Meta:
        model = CustomUser
        # 'password' must be included here to be accepted in the POST request
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'bio')

    # Custom create method to properly hash and save the password
    def create(self, validated_data):
        # The CustomUser manager handles create_user, hashing the password.
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', None)
        )
        return user

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