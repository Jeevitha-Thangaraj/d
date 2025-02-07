from rest_framework import serializers
from django.contrib.auth.models import User
from authentication.models import Profile

class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = "_all_"
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields="__all__"
    