import os
import datetime
import django
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "getxerpa.settings")
django.setup()

from getxerpa.finance.models import Category, Transaction

categories_data = [
    { "name": "Transportes", "limit": 1000},
    { "name": "Alimentacion", "limit": 5000},
]

transactions_data = [
    { "description": "Uber", "category": 1, "amount": 300, "ignore": False},
    { "description": "Burger King", "category": 2, "amount": 500,"ignore": True},
    { "description": "Taxi", "category": 1, "amount": 300,"ignore": False},
    { "description": "Restaurant Sol", "category": 2, "amount": 300,"ignore": False},
]

def populate():
   for category_data in categories_data:
        category = Category.objects.create(**category_data)

   for transaction_data in transactions_data:
        category_id = transaction_data.pop('category')
        category = Category.objects.get(pk=category_id)
        Transaction.objects.create(category=category, **transaction_data)


populate()