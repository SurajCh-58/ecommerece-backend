from django.urls import path
from cart.views import CartView,CartItemView

urlpatterns = [
    path('cart/',CartView.as_view(),name='cart'),
    path('cart-items/',CartItemView.as_view(),name='cart-items')
]
