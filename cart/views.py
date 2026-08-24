from cart.serializers import CartSerializer,CartItemCreateSerializer,CartItemReadSerializer
from rest_framework.generics import CreateAPIView,ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart,CartItem
# Create your views here.

class CartView(CreateAPIView):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemView(ListCreateAPIView):

    permission_classes=[IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method=="POST":
            return CartItemCreateSerializer
        return CartItemReadSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created=Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)