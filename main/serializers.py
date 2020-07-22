from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.state import User

from main.models import Category, Product, ShoppingCart


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom username claim
        token['username'] = user.username

        return token


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.ReadOnlyField(source='seller.username')

    class Meta:
        model = Product
        fields = '__all__'


class ProductViewSerializer(serializers.ModelSerializer):
    seller = serializers.ReadOnlyField(source='seller.username')
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['image']

    def save(self, **kwargs):
        if self.instance.image:
            self.instance.image.delete()
        return super().save(**kwargs)


# class ShoppingCartViewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ShoppingCart
#         fields = ['id', 'quantity', 'product']
#         depth = 1


class ShoppingCartSerializer(serializers.ModelSerializer):
    buyer = serializers.ReadOnlyField(source='buyer.username')

    class Meta:
        model = ShoppingCart
        fields = '__all__'
        depth = 1


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']


class ChangePasswordSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
