from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from main.permissions import IsUserOrReadOnly
from main.serializers import UserViewSerializer, UserSerializer, ChangePasswordSerializer, \
    UserCreateSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserViewSerializer
    permission_classes = (AllowAny,)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer: Serializer):
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            new_user = serializer.save()
            new_user.set_password(password)
            new_user.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        super().perform_create(serializer)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrReadOnly]


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password']},
                                status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response({'detail': 'Successfully changed password.', },
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
