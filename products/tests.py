from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from products.models import Product
from products.serializers import ProductSerializer


class ProductNaNHandlingTests(TestCase):
    def test_non_finite_dimensions_are_sanitized_to_zero_area(self):
        product = Product.objects.create(
            name='Test product',
            description='Test description',
            height=float('nan'),
            width=2.0,
            price='10.00',
            stock=1,
            image=SimpleUploadedFile(
                'test.jpg',
                b'fake-image-bytes',
                content_type='image/jpeg',
            ),
        )

        product.refresh_from_db()

        self.assertEqual(product.area, 0.0)
        self.assertEqual(ProductSerializer(instance=product).data['area'], 0.0)
