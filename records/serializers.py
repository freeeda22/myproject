# serializers.py
from rest_framework import serializers
from .models import ProductionData

class ProductionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionData
        fields = '__all__'
