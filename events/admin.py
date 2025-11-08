from django.contrib import admin
from .models import CartItems, Events, Tickets, Order, PurchasedTickets

# Register your models here.

@admin.register(PurchasedTickets)
class PurchasedTicketsAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'order', 'ticket', 'verified', 'get_event_name', 'get_customer_name')
    list_filter = ('verified', 'ticket__event', 'ticket__event__category')
    search_fields = ('unique_id', 'order__full_name', 'order__email_address', 'ticket__name', 'ticket__event__name')
    list_editable = ('verified',)
    ordering = ('-id',)
    
    def get_event_name(self, obj):
        return obj.ticket.event.name
    get_event_name.short_description = 'Event'
    get_event_name.admin_order_field = 'ticket__event__name'
    
    def get_customer_name(self, obj):
        return obj.order.full_name
    get_customer_name.short_description = 'Customer'
    get_customer_name.admin_order_field = 'order__full_name'

admin.site.register(CartItems)
admin.site.register(Events)
admin.site.register(Order)
admin.site.register(Tickets)
