from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="user_orders",
        default="")
    order_details = models.JSONField(default=None, null=True, blank=True)
    order_total = models.FloatField(default=None, null=True, blank=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"