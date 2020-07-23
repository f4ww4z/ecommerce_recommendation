from rest_framework_simplejwt.views import TokenObtainPairView

from main import serializers


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer
