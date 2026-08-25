from cart.serializers import CartItemCreateSerializer,CartItemUpdateSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart,CartItem
# Create your views here.

class CartItemView(ModelViewSet):

    permission_classes=[IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['update','partial_update']:
            return CartItemUpdateSerializer
        return CartItemCreateSerializer
       
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created=Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)