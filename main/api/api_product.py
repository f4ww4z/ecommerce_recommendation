from rest_framework import generics, views
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from main.models import Product
from main.serializers import ProductViewSerializer, ProductSerializer


class ProductList(generics.ListAPIView):
    serializer_class = ProductViewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Product.objects.exclude(seller_id=self.request.user.id)


class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductViewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# TODO: upload product image
class ProductImageUpload(views.APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
