from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    MyProductListView, MyProductDetailView,
    CategoryListView, ProductImageUploadView
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('my-products/', MyProductListView.as_view(), name='my-products'),
    path('my-products/<int:pk>/', MyProductDetailView.as_view(), name='my-product-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('images/', ProductImageUploadView.as_view(), name='product-image-upload'),
]