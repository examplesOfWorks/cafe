from django.shortcuts import render, redirect
from django.db.models import Prefetch
from orders.models import Orders, OrderItems
from orders.forms import CreateOrderForm, CreateOrderItemForm, CreateMealForm
from django.forms import ValidationError
from django.db import transaction
from django.contrib import messages

def show_orders(request):
    orders = (
        Orders.objects.all()
        .prefetch_related(
            Prefetch(
                "orderitems_set",
                queryset=OrderItems.objects.select_related('meal')
            )
        )
    )
    
    context = {
        'title': 'Все заказы',
        'orders': orders
    }
    
    return render(request, 'index.html', context)

def create_order(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                    
                order_form = CreateOrderForm(request.POST)
                tabel_number = request.POST.get('table_number')
                order_form.instance.table_number = tabel_number
                order_form.instance.status = "В ожидании"
                order_form.instance.total_price = 0
                order_form.save()

                for i in range(len(request.POST.getlist('name'))):
                    meal_form = CreateMealForm(request.POST)
                    order_item_form = CreateOrderItemForm(request.POST)
                    if meal_form.is_valid() and order_item_form.is_valid():
                        name = request.POST.getlist('name')
                        price = request.POST.getlist('price')
                        quantity = request.POST.getlist('quantity')
                        data = {'name': name[i], 'price': price[i], 'quantity': quantity[i]}
                        meal_form.instance.name = data['name']
                        meal_form.instance.price = data['price']
                        meal_form.save()
                            
                        order_item_form.instance.quantity = data['quantity']
                        order_item_form.instance.meal = meal_form.instance
                        order_item_form.instance.order = order_form.instance
                        order_item_form.instance.item_price = int(data['quantity']) * int(data['price'])
                        order_item_form.save()

                        order_form.instance.total_price += order_item_form.instance.item_price
                        order_form.save()

                messages.success(request, 'Заказ оформлен!')
                return redirect('/')

            else:
                order_form =CreateOrderForm()
                order_item_form = CreateOrderItemForm()
                meal_form = CreateMealForm()
                context = {
                    'order_form': order_form,
                    'order_item_form': order_item_form,
                    'meal_form': meal_form,
                }
                return render(request, 'create.html', context)

    except Exception:
        messages.error(request, 'Произошла ошибка.' )
        return redirect('orders:create_order')

def edit_status(request, id):
    context = {
        'title': 'Изменение статуса заказа',
    }
    
    return render(request, 'edit_status.html', context)

def delete_order(request, id):
    context = {
        'title': 'Удаление заказа',
    }
    
    return render(request, 'delete.html', context)