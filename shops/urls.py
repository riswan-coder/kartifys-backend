from django.urls import path
from .views import (
    ShopListView, ShopDetailView,
    ShopCreateView, MyShopView,
    AdminShopListView, ShopUpdateView,
    ShopDeleteView
)

urlpatterns = [
    path('', ShopListView.as_view(), name='shop-list'),
    path('create/', ShopCreateView.as_view(), name='shop-create'),
    path('my-shop/', MyShopView.as_view(), name='my-shop'),
    path('admin/all/', AdminShopListView.as_view(), name='admin-shop-list'),
    path('<int:pk>/', ShopDetailView.as_view(), name='shop-detail'),
    path('<int:pk>/update/', ShopUpdateView.as_view(), name='shop-update'),
    path('<int:pk>/delete/', ShopDeleteView.as_view(), name='shop-delete'),
]