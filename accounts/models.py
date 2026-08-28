from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        user=self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email,password,**extra_fields)

# Create your models here.
class User(AbstractUser):
    username=None
    first_name=None
    last_name=None
    email=models.EmailField(unique=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=UserManager()
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    full_name=models.CharField(max_length=100,blank=True,default='')
    image=models.ImageField(upload_to='profile_images/',blank=True,null=True)
    phone_number=PhoneNumberField(max_length=20,blank=True,default='')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

class Address(models.Model):
    class Label(models.TextChoices):
        HOME='home','Home'
        OFFICE='office','Office'
        OTHER='other','Other'
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="addresses")
    label=models.CharField(max_length=20,choices=Label.choices,default=Label.HOME)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    address_line=models.CharField(max_length=100)
    postal_code=models.CharField(max_length=20)
    is_default=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.label} {self.city}"