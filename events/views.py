from rest_framework import viewsets, parsers, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import CartItems, Events, Order, Tickets, PurchasedTickets
from .serializers import CartItemSerializer, EventSerializer, OrderSerializer, TicketSerializer
from .utils import send_email_with_purchased_tickets, notify_admin_of_purchase

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
        instance = serializer.save()
        
        email = serializer.validated_data.get("email_address")
        full_name = serializer.validated_data.get("full_name")
        order_id = instance.id
                
        cart_items_ids = request.data.get('cart_items', [])
        order_items = CartItems.objects.filter(id__in=cart_items_ids).select_related('ticket__event')

        # Create individual purchased tickets for each cart item quantity
        purchased_tickets = []
        
        for item in order_items:
            ticket = item.ticket
            # if ticket.quantity < item.quantity:
            #     raise serializers.ValidationError(
            #         f"Not enough tickets available for {ticket.name} (Available: {ticket.quantity}, Requested: {item.quantity})"
            #     )
            
            # Reduce ticket inventory
            ticket.quantity -= item.quantity
            ticket.save()
            
            # Create individual purchased tickets for each quantity
            for _ in range(item.quantity):
                purchased_ticket = PurchasedTickets.objects.create(
                    order=instance,
                    ticket=ticket,
                    verified=False
                )
                purchased_tickets.append(purchased_ticket)
            
        # Send email with individual PDFs for each purchased ticket
        send_email_with_purchased_tickets(email, instance, purchased_tickets)
        notify_admin_of_purchase(email, order_id, full_name)

        return Response(
            {
                "status": True, 
                "message": "Tickets purchased", 
                "data": serializer.data, 
                "account_details": {
                    "account_no": "2066176772",
                    "bank": "United Bank of Africa",
                    "account_name": "Okoroafor Emmanuel"
                }
            },
            status=status.HTTP_200_OK,
        )

