from rest_framework import viewsets, parsers, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import CartItems, Events, Order, Tickets
from .serializers import CartItemSerializer, EventSerializer, OrderSerializer, TicketSerializer

# Create your views here.

class EventViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    
    def get_permissions(self):
        # Only require authentication for write operations
        if self.request.method in ['POST', 'PATCH', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class = TicketSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    
    def get_permissions(self):
        # Only require authentication for write operations
        if self.request.method in ['POST', 'PATCH', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItems.objects.all()
    serializer_class = CartItemSerializer
    parser_classes = [parsers.JSONParser]
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"status": True, "message": "Ticket added to cart", "data": serializer.data},
            status=status.HTTP_200_OK,
        )
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"status": True, "message": "Ticket updated in cart", "data": serializer.data},
            status=status.HTTP_200_OK,
        )
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    parser_classes = [parsers.JSONParser]
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        cart_items_ids = request.data.get('cart_items', [])
        order_items = CartItems.objects.filter(id__in=cart_items_ids).select_related('ticket')

        for item in order_items:
            ticket = item.ticket
            # if ticket.quantity < item.quantity:
            #     raise serializers.ValidationError(
            #         f"Not enough tickets available for {ticket.name} (Available: {ticket.quantity}, Requested: {item.quantity})"
            #     )
            ticket.quantity -= item.quantity
            ticket.save()

        return Response(
            {
                "status": True, 
                "message": "Tickets purchased", 
                "data": serializer.data, 
                "account_details": {
                    "account_no": "00092949499",
                    "bank": "WEMA",
                    "account_name": "JOHN DOE"
                }
            },
            status=status.HTTP_200_OK,
        )

