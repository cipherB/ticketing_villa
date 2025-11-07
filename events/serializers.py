from rest_framework import serializers
from django.conf import settings
import cloudinary
from .models import CartItems, Events, Order, Tickets

class TicketSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tickets
        fields = ['id', 'name', 'deadline', 'price', 'quantity', 'description']
        
class EventSerializer(serializers.ModelSerializer):
    banner_link_url = serializers.SerializerMethodField()
    tickets = TicketSerializer(many=True, read_only=True)
    
    class Meta:
        model = Events
        fields = ['id', 'name', 'description', 'category', 'banner_url', 'event_date', 'event_time', 'venue_name', 'address', 'tickets', "banner_link_url"]
    
    def get_banner_link_url(self, obj):
        if obj.banner:
            # Complete the Cloudinary URL
            banner_path = str(obj.banner)
            if banner_path and not banner_path.startswith('http'):
                cloud_name = cloudinary.config().cloud_name
                return f"https://res.cloudinary.com/{cloud_name}/{banner_path}"
            return banner_path
        return None
    
class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItems
        fields = "__all__"
        

class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = "__all__"
    