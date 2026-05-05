from rest_framework import serializers
from .models import Ad
from shops.serializers import ShopSerializer
from shops.models import Shop


class AdSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(read_only=True)
    shop_id = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(),
        source='shop',
        write_only=True
    )
    image_url = serializers.SerializerMethodField()
    slot_label = serializers.CharField(
        source='get_slot_display',
        read_only=True
    )

    class Meta:
        model = Ad
        fields = [
            'id', 'shop', 'shop_id', 'slot', 'slot_label',
            'image', 'image_url', 'is_active', 'created_at'
        ]
        extra_kwargs = {
            'image': {'required': False}
        }

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None