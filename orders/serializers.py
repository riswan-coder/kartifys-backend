from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    subtotal = serializers.ReadOnlyField()
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False
    )

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_id',
            'quantity', 'price', 'size', 'color', 'subtotal'
        ]

    def get_product(self, obj):
        if obj.product:
            return {
                'id': obj.product.id,
                'name': obj.product.name,
                'price': str(obj.product.price),
                'shop_name': obj.product.shop.name,
            }
        return None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.ReadOnlyField()
    customer_name = serializers.CharField(
        source='customer.username',
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'status',
            'delivery_address', 'delivery_phone',
            'delivery_pincode', 'note',
            'cancel_reason', 'items',
            'total_price', 'created_at'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(
            customer=self.context['request'].user,
            **validated_data
        )
        for item_data in items_data:
            product = item_data['product']
            price = item_data.get('price') or product.price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data.get('quantity', 1),
                price=price,
                size=item_data.get('size', ''),
                color=item_data.get('color', ''),
            )
        return order