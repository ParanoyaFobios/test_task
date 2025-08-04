from django.db import models


class Product(models.Model):
    title = models.CharField(null=True)
    current_price = models.DecimalField(null=True)
    original_price = models.DecimalField(null=True)
    discount = models.FloatField(null=True)
    rating = models.FloatField(null=True)  
    reviews = models.FloatField(null=True)
    delivery = models.BooleanField(default=True)
    seller = models.CharField(null=True)
    product_url = models.URLField(null=True)


    def __str__(self):
        return self.title