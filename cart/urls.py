from django.urls import path,include
from cart.views import CartItemView
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register(r'cart-items',CartItemView,basename='cart_items')

urlpatterns = [
    path('',include(router.urls)),
]
