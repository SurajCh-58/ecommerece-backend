from rest_framework.generics import RetrieveAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import ProfileSerializer,UserSerializer
from allauth.headless.contrib.rest_framework.authentication import JWTTokenAuthentication

# Create your views here.

class ProfileView(RetrieveAPIView):
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTTokenAuthentication]

    def get_object(self):
        return self.request.user

class ProfileUpdateView(RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTTokenAuthentication]

    def get_object(self):
        return self.request.user.profile