from rest_framework import serializers
from .models import Shop
from accounts.models import User
from accounts.serializers import UserSerializer


class ShopSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    product_count = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = [
            'id', 'name', 'description', 'address',
            'city', 'phone', 'email', 'logo', 'logo_url',
            'category', 'is_active', 'owner',
            'product_count', 'created_at'
        ]
        extra_kwargs = {
            'logo': {'required': False}
        }

    def get_product_count(self, obj):
        return obj.products.filter(is_available=True).count()

    def get_logo_url(self, obj):
        if obj.logo:
            try:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.logo.url)
                return obj.logo.url
            except Exception:
                return None
        return None


class ShopCreateSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='shop_owner'),
        source='owner',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Shop
        fields = [
            'name', 'description', 'address',
            'city', 'phone', 'email', 'owner_id', 'category'
        ]

    def validate_owner_id(self, value):
        if value and Shop.objects.filter(owner=value).exists():
            raise serializers.ValidationError(
                "This user already owns a shop."
            )
        return value