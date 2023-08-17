from django.db import models
from django.utils import timezone

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    limit = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'finance'
    def __str__(self):
        return self.name

class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now_add=True)
    ignore = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'finance'
    def __str__(self):
        return self.description
