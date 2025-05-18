from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class EventCategories(models.TextChoices):
    BEACH_PARTY = 'BEACH_PARTY', 'BEACH PARTY'
    BLOCK_PARTY = 'BLOCK_PARTY', 'BLOCK PARTY'

class Events(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(
        max_length=25,
        choices=EventCategories.choices,
        default=""
    )
    banner = CloudinaryField('image', null=True, blank=True)
    banner_url = models.SlugField(blank=True, null=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    venue_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField()
    
    def __str__(self):
        return self.name
    
class Tickets(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='tickets')
    deadline = models.DateTimeField()
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class CartItems(models.Model):
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE, related_name='cart_item')
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    
    def __str__(self):
        return f"{self.ticket.name} - {self.ticket.event.name}"
    
class Order(models.Model):
    full_name = models.CharField(max_length=100)
    email_address = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    cart_items = models.ManyToManyField(CartItems)
    total = models.FloatField()
    payment_status = models.BooleanField(default=False)
    payment_receipt = CloudinaryField('image', blank=True, null=True)
    payment_receipt_url = models.SlugField(blank=True, null=True)
    paid_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name}"
    

    