"""
import json
import statistics
import math
from datetime import datetime
from collections import defaultdict
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Sum
from functions.models.supplier import Supplier
from functions.models.material import Material
from functions.models.materialSource import MaterialSource
from functions.models.product import Product
from functions.models.ingredient import Ingredient
from functions.models.inventory import Inventory
from functions.models.customer import Customer
from functions.models.order import Order
from functions.models.orderDetail import OrderDetail


def deductInventory(order):
    orderDetails = OrderDetail.objects.filter(order=order)
    for orderDetail in orderDetails:
        ingredients = Ingredient.objects.filter(product=orderDetail.product)
        for ingredient in ingredients:
            inventories = Inventory.objects.filter(material=ingredient.material).order_by('importDate')
            remainAmount = int(orderDetail.amount) * int(ingredient.unit)
            with transaction.atomic():
                for inventory in inventories:
                    if remainAmount <= 0:
                        break

                    if inventory.importAmount > remainAmount:
                        inventory.importAmount -= remainAmount
                        inventory.save()
                    else:
                        remainAmount -= inventory.importAmount
                        inventory.delete()
            if remainAmount > 0:
                raise ValueError(f"存貨不足：需要 {int(orderDetail.amount) * int(ingredient.unit)}，但可用存貨不足。")
"""
