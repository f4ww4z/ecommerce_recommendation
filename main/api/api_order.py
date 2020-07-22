from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from main.models import Order, Product
from main.permissions import IsBuyer
from main.serializers import OrderSerializer, OrderUpdateSerializer


class OrderListCreate(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(buyer_id=user.id)

    def perform_create(self, serializer):
        data = self.request.data
        product_id = data['product']
        quantity = data['quantity']

        product = Product.objects.get(pk=product_id)
        total_price = product.price * quantity

        serializer.save(buyer=self.request.user, product=product, total_price=total_price)


class OrderUpdate(generics.UpdateAPIView):
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsBuyer]
    queryset = Order.objects.all()
