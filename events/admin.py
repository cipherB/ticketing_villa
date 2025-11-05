from django.contrib import admin
from .models import CartItems, Events, Tickets, Order, PurchasedTickets

# Register your models here.
admin.site.register(CartItems)
admin.site.register(Events)
admin.site.register(Order)
admin.site.register(Tickets)
admin.site.register(PurchasedTickets)
