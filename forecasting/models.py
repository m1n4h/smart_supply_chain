from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    current_stock = models.IntegerField()
    unit_price_tzs = models.FloatField()

    class Meta:
        db_table = 'forecasting_product'

class SalesHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    quantity_sold = models.IntegerField()
    traffic_heavy = models.IntegerField()
    weather_delay = models.IntegerField()

    class Meta:
        db_table = 'forecasting_saleshistory'