from rest_framework.generics import RetrieveAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import ProfileSerializer,UserSerializer, AddressSerializer
from rest_framework.viewsets import ModelViewSet
from accounts.models import Address

# Create your views here.

class ProfileView(RetrieveAPIView):
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]

    def get_object(self):
        return self.request.user

class ProfileUpdateView(RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class AddressView(ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user).order_by("-default","-created_at")
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)