from rest_framework_simplejwt.views import TokenObtainSlidingView

from main import serializers


class MyTokenObtainSlidingView(TokenObtainSlidingView):
    serializer_class = serializers.MyTokenObtainPairSerializer
