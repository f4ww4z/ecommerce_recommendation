from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from main import serializers


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = serializers.MyTokenObtainPairSerializer
