from rest_framework import serializers
from .models import CartItems, Events, Order, Tickets

class TicketSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tickets
        fields = ['id', 'name', 'deadline', 'price', 'quantity', 'description']
        
class EventSerializer(serializers.ModelSerializer):
    # banner_url = serializers.SerializerMethodField()
    tickets = TicketSerializer(many=True, read_only=True)
    
    class Meta:
        model = Events
        fields = ['id', 'name', 'description', 'category', 'banner_url', 'event_date', 'event_time', 'venue_name', 'address', 'tickets']
    
    # def get_banner_url(self, obj):
    #     if obj.banner:
    #         return obj.banner.url
    #     return None
    
class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItems
        fields = "__all__"
        

class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = "__all__"
    