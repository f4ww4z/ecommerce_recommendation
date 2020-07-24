from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import ShoppingCart, Product
from main.serializers import ShoppingCartSerializer


class RetrieveOrAddToShoppingCart(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        user = self.request.user
        return ShoppingCart.objects.filter(buyer_id=user.id)

    def perform_create(self, serializer):
        data = self.request.data
        product_id = data['product']
        quantity = data['quantity']
        if quantity <= 0:
            raise ValidationError({'message': 'Quantity must be greater than 0!'})

        # if product already exists in cart, add the quantity
        my_cart: QuerySet = self.get_queryset()
        if my_cart.filter(product_id=product_id).exists():
            cart_to_update = my_cart.get(product_id=product_id)
            cart_to_update.quantity += quantity
            cart_to_update.save()
            return

        product = Product.objects.get(pk=product_id)
        serializer.save(buyer=self.request.user, product=product)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def retrieve_modify_shopping_cart(request, product_id: int):
    user = request.user

    if request.method == 'PUT':
        quantity = request.data['quantity']
        cart = ShoppingCart.objects.get(buyer_id=user.id, product_id=product_id)
        cart.quantity = quantity
        cart.save()
        serializer = ShoppingCartSerializer(cart)
        return Response(serializer.data)

    # to remove product from shopping cart
    elif request.method == 'DELETE':
        cart = ShoppingCart.objects.get(buyer_id=user.id, product_id=product_id)
        cart.delete()
        return Response({'message': 'Product removed from cart.'})
