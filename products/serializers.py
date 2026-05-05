from rest_framework import serializers
from .models import Product, Category, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'gender', 'product_type']


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_file = serializers.ImageField(
        write_only=True,
        source='image',
        required=True
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=True
    )
    is_primary = serializers.BooleanField(default=False)

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_file', 'product', 'is_primary']

    def get_image(self, obj):
        if obj.image:
            try:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.image.url)
                return f"http://172.20.10.3:8000{obj.image.url}"
            except Exception as e:
                print(f"Image error: {e}")
                return None
        return None

    def create(self, validated_data):
        print("Creating image with data:", validated_data)
        return ProductImage.objects.create(**validated_data)

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    shop_name = serializers.CharField(source='shop.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price',
            'stock', 'sizes', 'colors', 'is_available',
            'category', 'category_id', 'images',
            'shop_name', 'created_at'
        ]
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price',
            'stock', 'sizes', 'colors', 'is_available',
            'category', 'category_id', 'images',
            'shop_name', 'created_at'
        ]

    def create(self, validated_data):
        # Automatically assign to the shop owner's shop
        shop = self.context['request'].user.shop
        validated_data['shop'] = shop
        return super().create(validated_data)