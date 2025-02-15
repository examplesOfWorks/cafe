from django.contrib import admin
from .models import Meals, Orders, OrderItems

@admin.register(Meals)
class MealsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'total_price', 'status', 'created_timestamp')


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'meal', 'quantity')

