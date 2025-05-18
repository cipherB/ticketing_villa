from django.contrib import admin
from .models import CartItems, Events, Tickets, Order

# Register your models here.
admin.site.register(CartItems)
admin.site.register(Events)
admin.site.register(Order)
admin.site.register(Tickets)
