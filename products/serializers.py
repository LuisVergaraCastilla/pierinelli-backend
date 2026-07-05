import math

from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('area',)  # Area is calculated in the model

    @staticmethod
    def _sanitize_float(value):
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            return 0.0

        if not math.isfinite(numeric_value):
            return 0.0

        return numeric_value

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        for field_name in ('height', 'width', 'area'):
            if field_name in representation:
                representation[field_name] = self._sanitize_float(representation[field_name])

        return representation
