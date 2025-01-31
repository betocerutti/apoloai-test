from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model, contains all fields.
    Covers CRUD operations.
    """

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class UpdateStockSerializer(serializers.Serializer):
    """
    Serializer for updating the stock, only contains the stock field.
    """
    class Meta:
            model = Product
            fields = ['stock']