from rest_framework import serializers
from .models import CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='dishes.name')
    product_id = serializers.CharField(source='dishes.id')
    product_image = serializers.CharField(source='dishes.photolink')
    cost = serializers.SerializerMethodField()
    product_grams = serializers.CharField(source='dishes.grams')

    class Meta:
        model = CartItem
        fields = ['product_id','product_name', 'quantity', 'cost', 'product_image', 'product_grams']

    def get_cost(self, obj):
        return obj.get_cost()