from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer, UpdateStockSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        method="patch",
        operation_description="Update the stock of a specific product",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "stock": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="New stock value"
                ),
            },
            required=["stock"],
        ),
        responses={
            200: ProductSerializer(),
            400: "Bad Request (e.g., missing stock value or invalid data)",
            404: "Product not found",
        },
    )
    @action(detail=True, methods=["patch"], url_path="update-stock")
    def update_stock(self, request, pk=None):
        try:
            product = self.get_object()
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Use the custom serializer to validate and update the stock
        serializer = UpdateStockSerializer(product, data=request.data, partial=True)

        # Get the new stock value from the request
        new_stock = request.data.get("stock", None)
        if new_stock is None:
            return Response(
                {"error": "stock is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Update the stock value
        product.stock = new_stock
        product.save()

        # Return the updated product
        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Retrieve a list of all products",
        responses={200: ProductSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a single product by ID",
        responses={200: ProductSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
