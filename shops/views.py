from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Shop
from .serializers import ShopSerializer, ShopCreateSerializer
from accounts.models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )


class IsShopOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'shop_owner'
        )


class ShopListView(generics.ListAPIView):
    serializer_class = ShopSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Shop.objects.filter(is_active=True)
        city = self.request.query_params.get('city')
        search = self.request.query_params.get('search')
        category = self.request.query_params.get('category')

        if city:
            queryset = queryset.filter(city__icontains=city)
        if search:
            queryset = queryset.filter(name__icontains=search)
        if category:
            queryset = queryset.filter(category=category)

        # Random order every time
        return queryset.order_by('?')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ShopDetailView(generics.RetrieveAPIView):
    serializer_class = ShopSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Shop.objects.filter(is_active=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ShopCreateView(generics.CreateAPIView):
    serializer_class = ShopCreateSerializer
    permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        print(f"User: {request.user}, Role: {request.user.role}, Auth: {request.user.is_authenticated}")
        return super().create(request, *args, **kwargs)


class MyShopView(generics.RetrieveUpdateAPIView):
    serializer_class = ShopSerializer
    permission_classes = [IsShopOwner]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self):
        return Shop.objects.get(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class AdminShopListView(generics.ListAPIView):
    serializer_class = ShopSerializer
    permission_classes = [IsAdmin]
    queryset = Shop.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ShopUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ShopSerializer
    permission_classes = [IsAdmin]
    queryset = Shop.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
class ShopDeleteView(generics.DestroyAPIView):
    serializer_class = ShopSerializer
    permission_classes = [IsAdmin]
    queryset = Shop.objects.all()