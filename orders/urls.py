from django.urls import path
from orders.views import OrderCreateView, OrderListView, OrderReteriveView

urlpatterns = [
    path('create/',OrderCreateView.as_view(),name='order_create'),
    path('all/',OrderListView.as_view(),name='all_order'),
    path('<int:pk>/',OrderReteriveView.as_view(),name='single_order')   
]
