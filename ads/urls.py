from django.urls import path
from .views import (
    ActiveAdView, AllActiveAdsView,
    PopupAdView, BannerAdsView,
    AdListView, AdDetailView
)

urlpatterns = [
    path('active/', ActiveAdView.as_view(), name='active-ad'),
    path('all-active/', AllActiveAdsView.as_view(), name='all-active-ads'),
    path('popup/', PopupAdView.as_view(), name='popup-ad'),
    path('banners/', BannerAdsView.as_view(), name='banner-ads'),
    path('', AdListView.as_view(), name='ad-list'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
]