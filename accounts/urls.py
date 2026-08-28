from django.urls import path,include
from .views import ProfileView,ProfileUpdateView, AddressView
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'address',AddressView,basename='address')

urlpatterns=[
    path('profile/',ProfileView.as_view(),name='profile'),
    path('profile/update/',ProfileUpdateView.as_view(),name='profile-update'),
    path('profile/',include(router.urls))
]