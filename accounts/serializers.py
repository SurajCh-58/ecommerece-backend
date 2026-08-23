from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Profile
from common.utils import validate_image

User=get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['full_name','image','phone_number']

    def validate_image(self,image):
        return validate_image(image)

class UserSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=User
        fields=['email','profile']
