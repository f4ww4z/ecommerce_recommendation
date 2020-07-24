from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from main.models import Order, OrderGroup, ShoppingCart
from main.permissions import IsBuyer
from main.serializers import OrderSerializer, OrderUpdateSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_items_in_shopping_cart(request):
    user = request.user
    shopping_cart = ShoppingCart.objects.filter(buyer_id=user.id)

    if len(shopping_cart) == 0:
        return JsonResponse({'message': 'No items in shopping cart.'})

    new_order_group = OrderGroup.objects.create(buyer=user)
    new_order_group.save()

    total_price = 0.0

    for item in shopping_cart:
        item_total_price = item.product.price * item.quantity
        order = Order.objects.create(
            buyer=user,
            product=item.product,
            quantity=item.quantity,
            total_price=item_total_price,
            order_group=new_order_group
        )
        order.save()
        total_price += item_total_price

        item.delete()

    new_order_group.total_price = total_price
    new_order_group.save()

    return JsonResponse({'message': 'Successfully bought items in shopping cart.'},
                        status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_group_list(request):
    order_groups = OrderGroup.objects.filter(buyer_id=request.user.id)

    response_dict = []

    for order_group in order_groups:
        response_order_group_dict = {
            'id': order_group.id,
            'date_time_ordered': order_group.date_time_ordered,
            'total_price': order_group.total_price,
            'orders': []
        }

        orders = Order.objects.filter(order_group=order_group)

        for order in orders:
            p = order.product
            response_order_dict = {
                'id': order.id,
                'product': {
                    'id': p.id,
                    'name': p.name,
                    'price': p.price
                },
                'quantity': order.quantity,
                'total_price': order.total_price,
                'status': order.status
            }

            response_order_group_dict['orders'].append(response_order_dict)

        response_dict.append(response_order_group_dict)

    return JsonResponse(response_dict, safe=False)


class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(buyer_id=user.id)


class OrderUpdate(generics.UpdateAPIView):
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsBuyer]
    queryset = Order.objects.all()
