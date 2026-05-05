from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Product, Category, ProductImage
from .serializers import ProductSerializer, CategorySerializer, ProductImageSerializer


class IsShopOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'shop_owner'
        )


from django.db.models import Q

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        gender = self.request.query_params.get('gender')
        product_type = self.request.query_params.get('type')
        shop_id = self.request.query_params.get('shop')
        search = self.request.query_params.get('search', '').strip()

        if gender:
            queryset = queryset.filter(category__gender=gender)
        if product_type:
            queryset = queryset.filter(category__product_type=product_type)
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)

        if search:
            # Split search into individual words
            # Example: "black linen shirt" → ["black", "linen", "shirt"]
            words = search.split()

            for word in words:
                queryset = queryset.filter(
                    Q(name__icontains=word) |
                    Q(description__icontains=word) |
                    Q(colors__icontains=word) |
                    Q(sizes__icontains=word) |
                    Q(shop__name__icontains=word) |
                    Q(category__gender__icontains=word) |
                    Q(category__product_type__icontains=word)
                )

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.filter(is_available=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class MyProductListView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsShopOwner]

    def get_queryset(self):
        return Product.objects.filter(shop__owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class MyProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsShopOwner]

    def get_queryset(self):
        return Product.objects.filter(shop__owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.all()


class ProductImageUploadView(generics.CreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [IsShopOwner]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        print("Image upload data:", request.data)
        print("Image upload files:", request.FILES)
        return super().create(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context