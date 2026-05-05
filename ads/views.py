from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Ad
from .serializers import AdSerializer


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )


# Slot 1 — popup ad on app open
class PopupAdView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        ad = Ad.objects.filter(
            is_active=True,
            slot='slot_1'
        ).first()
        if ad:
            serializer = AdSerializer(ad, context={'request': request})
            return Response(serializer.data)
        return Response(None)


# Slot 2 — banner ads in home screen
class BannerAdsView(generics.ListAPIView):
    serializer_class = AdSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Ad.objects.filter(is_active=True, slot='slot_2')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# Admin — manage all ads
class AdListView(generics.ListCreateAPIView):
    serializer_class = AdSerializer
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    queryset = Ad.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdSerializer
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    queryset = Ad.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# Keep for backwards compatibility
class ActiveAdView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        ad = Ad.objects.filter(is_active=True, slot='slot_1').first()
        if ad:
            serializer = AdSerializer(ad, context={'request': request})
            return Response(serializer.data)
        return Response(None)


class AllActiveAdsView(generics.ListAPIView):
    serializer_class = AdSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Ad.objects.filter(is_active=True, slot='slot_2')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context