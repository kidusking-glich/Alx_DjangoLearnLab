from rest_framework import serializers
from .models import CustomUser


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password =serializers.CharField(write_only=True)

    class Meta:
        model =CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'bio')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username= validated_data['username'],
            email = validated_data('email', ''),
            password=validated_data('password'),
        )
        return user 
    
class CustomUserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model =CustomUser
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name','bio', 'prfile_picture',
            'followers_count', 'following_count'
        )
        read_only_fields = ('username', 'email', 'followers_count', 'following_count')

        def get_followers_count(self, obj):
            return obj.followers.count()
        
        def get_following_count(self, obj):
            return obj.following.count()#'following' is the related_name