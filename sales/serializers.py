from rest_framework import serializers
from .models import Sale
from users.serializers import UserLiteSerializer
from products.serializers import ProductSerializer

class SaleSerializer(serializers.ModelSerializer):
    worker = UserLiteSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = '__all__'

class SaleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ('product', 'quantity')
