from django.contrib import admin
from accounts.models import User,Profile
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('id','email','is_staff','is_superuser','is_active','date_joined')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','full_name','phone_number','image','created_at','updated_at')