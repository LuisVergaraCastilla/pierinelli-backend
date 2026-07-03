from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Sale
from .serializers import SaleSerializer, SaleCreateSerializer
from users.permissions import IsAdmin, IsWorker
from products.models import Product

class SaleViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsWorker]
        else: # list
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = Sale.objects.select_related('product', 'worker').all()
        serializer = SaleSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = SaleCreateSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']

            if product.stock < quantity:
                return Response(
                    {'error': True, 'message': f'Insufficient stock. Available: {product.stock}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                sale = Sale.objects.create(
                    product=product,
                    worker=request.user,
                    quantity=quantity,
                    unit_price=product.price
                )
                
                product.stock -= quantity
                product.save()

                low_stock_threshold = 3 
                low_stock = product.stock <= low_stock_threshold

                response_data = SaleSerializer(sale).data
                response_data['low_stock'] = low_stock

                return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
