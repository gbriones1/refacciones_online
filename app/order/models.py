from django.db import models

from app.product.models import Product
from app.account.models import UserProfile

class Order(models.Model):

    CANCELED_STATUS = "c"
    DELIVERED_STATUS = "d"
    SHIPPED_STATUS = "s"
    RETURNED_STATUS = "r"
    ON_WAY_STATUS = "o"

    STATUS_CHOICES = (
        (CANCELED_STATUS,"Cancelado"),
        (DELIVERED_STATUS, "Entregado"),
        (SHIPPED_STATUS,"Enviado"),
        (RETURNED_STATUS, "Devuelto"),
        (ON_WAY_STATUS, "En camino"),
    )

    profile = models.ForeignKey(UserProfile, null=False)
    product = models.ManyToManyField(Product, through="Order_Product")
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
    paid = models.BooleanField(default=False, null=False)
    charge = models.DecimalField(max_digits=12, decimal_places=2)

class Order_Product(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(null=False, blank=False)