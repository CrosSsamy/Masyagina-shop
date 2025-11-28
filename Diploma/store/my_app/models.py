from django.db import models

# Create your models here.
class Games(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    info = models.TextField()
    img = models.CharField(max_length=100, blank=True)

class Cart(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    img = models.CharField(max_length=100, blank=True)