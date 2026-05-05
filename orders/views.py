from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer


class IsShopOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'shop_owner'


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class MyOrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class MyOrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class ShopOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsShopOwner]

    def get_queryset(self):
        return Order.objects.filter(
            items__product__shop__owner=self.request.user
        ).distinct()


class UpdateOrderStatusView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsShopOwner]
    http_method_names = ['patch']

    def get_queryset(self):
        return Order.objects.filter(
            items__product__shop__owner=self.request.user
        ).distinct()


class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdmin]
    queryset = Order.objects.all()


# Shop owner cancel order with reason
class CancelOrderView(APIView):
    permission_classes = [IsShopOwner]

    def post(self, request, pk):
        reason = request.data.get('reason', '').strip()

        if not reason:
            return Response(
                {'error': 'Cancellation reason is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.filter(
                items__product__shop__owner=request.user
            ).distinct().get(pk=pk)

            if order.status in ['delivered', 'cancelled']:
                return Response(
                    {'error': f'Cannot cancel an order that is already {order.status}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            order.status = 'cancelled'
            order.cancel_reason = reason
            order.save()

            return Response({
                'message': 'Order cancelled successfully',
                'order_id': order.id,
                'reason': reason
            })

        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )