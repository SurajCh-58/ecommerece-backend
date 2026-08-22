from PIL import Image
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Profile

User=get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['full_name','image','phone_number']

    def validate_image(self,image):
        if image.size>2*1024*1024:
            raise serializers.ValidationError("Image size must be less than 2 MB.")
        try:
            img=Image.open(image)
            img.verify()

            image.seek(0)

            img=Image.open(image)

        except Exception:
            raise serializers.ValidationError("The uploaded file is not a valid image.")
        if img.format not in ['JPEG','PNG','WEBP']:
            raise serializers.ValidationError("Only JPEG, PNG, and WEBP images are supported.")
        return image
    
class UserSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=User
        fields=['email','profile']

    def validate_email(self,value):
        email=value.strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email already registered.")
        return email

