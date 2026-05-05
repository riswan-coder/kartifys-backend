from django.urls import path
from .views import (
    MyOrderListView, MyOrderDetailView,
    ShopOrderListView, UpdateOrderStatusView,
    AdminOrderListView, CancelOrderView
)

urlpatterns = [
    path('my/', MyOrderListView.as_view()),
    path('my/<int:pk>/', MyOrderDetailView.as_view()),
    path('shop/', ShopOrderListView.as_view()),
    path('shop/<int:pk>/update/', UpdateOrderStatusView.as_view()),
    path('shop/<int:pk>/cancel/', CancelOrderView.as_view()),
    path('admin/all/', AdminOrderListView.as_view()),
]