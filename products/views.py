from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from users.permissions import IsAdminOrAuthenticatedReadOnly

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly]
