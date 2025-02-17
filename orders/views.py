from django.db import transaction
from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect, HttpResponseRedirect
from orders.search_utils import q_search, filter_by_status
from orders.models import Orders, OrderItems
from orders.forms import CreateOrderForm, CreateOrderItemForm, CreateMealForm, EditStatusForm


def show_orders(request) -> HttpResponse:
    """
    Функция для отображения страницы со всеми заказами. Здесь можно
    фильтровать заказы по статусу, а также производить поиск по номеру стола
    или статусу.

    Принимает: 
        request
    
    Возвращает:
        Страница со всеми заказами
    """
    query = request.GET.get('q', None)  

    waiting = request.GET.get('waiting', None)
    ready = request.GET.get('ready', None)
    paid = request.GET.get('paid', None)

    # фильтрация
    if waiting or ready or paid:
        orders = filter_by_status(waiting, ready, paid)

    # поиск
    elif query:
        orders = q_search(query).prefetch_related(
            Prefetch(
                "orderitems_set",
                queryset=OrderItems.objects.select_related('meal')
            )
        )
    # отображение всех заказов
    else:
        orders = (
        Orders.objects.all()
        .prefetch_related(
            Prefetch(
                "orderitems_set",
                queryset=OrderItems.objects.select_related('meal')
            )
        )
    )
    context: dict = {
        'title': 'Все заказы',
        'orders': orders,
    }
    return render(request, 'index.html', context)

def create_order(request) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    """
    Функция для создания нового заказа. Создает новый заказ с уникальным ID, указанным номером стола и статусом "В ожидании".
    Также происходит добавление блюд и связывание их с заказом.

    Принимает: 
        request
        
    Возвращает: 
        Перенаправление на страницу со всеми заказами если заказ успешно создан или
        отображение той же страницы, если произошла ошибка
    """
    try:
        with transaction.atomic():

            if request.method == 'POST':
                # создание заказа
                order_form = CreateOrderForm(request.POST)
                tabel_number = request.POST.get('table_number')
                order_form.instance.table_number = tabel_number
                order_form.instance.status = "В ожидании"
                order_form.instance.total_price = 0
                order_form.save()
                
                # добавление блюд и связывание их с заказом
                for i in range(len(request.POST.getlist('name'))):
                    meal_form = CreateMealForm(request.POST)
                    order_item_form = CreateOrderItemForm(request.POST)
                    if meal_form.is_valid() and order_item_form.is_valid():
                        name = request.POST.getlist('name')
                        price = request.POST.getlist('price')
                        quantity = request.POST.getlist('quantity')
                        data: dict = {'name': name[i], 'price': price[i], 'quantity': quantity[i]}
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
                # создание форм при открытии страницы
                order_form =CreateOrderForm()
                order_item_form = CreateOrderItemForm()
                meal_form = CreateMealForm()
                context: dict = {
                    'order_form': order_form,
                    'order_item_form': order_item_form,
                    'meal_form': meal_form,
                }
                return render(request, 'create.html', context)

    except Exception:
        messages.error(request, 'Произошла ошибка.' )
        return redirect('orders:create_order')

def edit_status(request, id) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse | None:
    """
    Функция для изменения статуса заказа

    Принимает:
        request (HttpRequest): request object
        id (int): id заказа

    Возвращает:
        Перенаправление на страницу со всеми заказами если статус успешно изменен или
            отображение страницы 404 если заказ не был найден
    """
    statuses_list: list[str] = ['В ожидании', 'Готово', 'Оплачено']

    orders = Orders.objects.filter(pk=id).prefetch_related(
            Prefetch(
                "orderitems_set",
                queryset=OrderItems.objects.select_related('meal')
            )
        )
    
    try:
        old_data = get_object_or_404(Orders, id=id)
    except Exception:
        raise Http404('Такого заказа не существует')

    if request.method =='POST':
        form = EditStatusForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = EditStatusForm(instance = old_data)
        context: dict = {
            'form':form,
            'statuses_list': statuses_list,
            'title': 'Изменение статуса',
            'orders': orders
        }
        return render(request, 'edit_status.html', context)
    
def edit_order(request, id) -> HttpResponse:
    """
    Функция для отображения страницы с вариантами возможностей редактирования заказа. 
    Если заказ с заданным id не был найден, отображается страница 404

    Принимает:
        request (HttpRequest): request object
        id (int): id заказа

    Возвращает:
        HttpResponse: Страница с вариантами возможностей редактирования заказа. 
    """
    try:
        get_object_or_404(Orders, id=id)
    except Exception:
        raise Http404('Такого заказа не существует')
    
    
    orders = Orders.objects.filter(pk=id).prefetch_related(
        Prefetch(
        "orderitems_set",
        queryset=OrderItems.objects.select_related('meal')
        )
    )
    meal_form = CreateMealForm()
    context: dict = {
        'title': 'Редактирование заказа',
        'orders': orders,
        'meal_form': meal_form
    }

    return render(request, 'edit_order.html', context)

def delete_order(request, id):
    """
    Осуществляет удаление заказа. Если заказ с указанным id существует,
    он и связанные с ним элементы удаляются. 

    Принимает:
        request (HttpRequest): request
        id (int): id заказа, который нужно удалить.

    Возвращает:
        HttpResponse: Редирект на страницу со всеми заказами, если заказ успешно удален. 
        Перед удалением заказа запрашивается подтверждение действия.

    Raises:
        Http404: отображение страницы 404, если заказ с указанным id не был найден.
    """
    try:
        data: Orders = get_object_or_404(Orders, id=id)
    except Exception:
        raise Http404('Такого заказа не существует')

    if request.method == 'POST':
        items = OrderItems.objects.filter(order=data)
        for item in items:
            item.meal.delete()
        data.delete()
        messages.success(request, 'Заказ удален')
        return redirect('/')
    else:
        context: dict[str, str] = {
            'title': 'Удаление заказа',
        }
        
        return render(request, 'delete.html', context)
    
def delete_item(request, id):
    """
    Осуществляет удаление отдельного блюда (позиции) из заказа. 
    Если блюдо с указанным id существует, оно и связанные с ним элементы 
    удаляются. 

    Принимает:
        request (HttpRequest): request
        id (int): id позиции, которую нужно удалить.

    Возвращает:
        HttpResponse: Редирект на страницу с заказом, если позиция успешно удалена. 
        Перед удалением позиции запрашивается подтверждение действия.

    Raises:
        Http404: отображение страницы 404, если блюда с указанным id не было найдено.
    """
    try:
        data: OrderItems = get_object_or_404(OrderItems, id=id)
    except Exception:
        raise Http404('Блюда с таким id не существует')
    
    if request.method == 'POST':
        data.order.total_price = int(data.order.total_price) - int(data.item_price)
        data.order.save()
        data.meal.delete()
        data.delete()
        messages.success(request, 'Блюдо удалено')
        return redirect(f'/edit-order/{int(data.order.id)}')
    else:
        context: dict[str, str] = {
            'title': 'Удаление позиции заказа',
        }
        
        return render(request, 'delete_item.html', context)
    
def add_items(request, id) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    """
    Осуществляет добавление одного или нескольких блюд (позиций) к заказу. 
    Если данные формы валидны, то они добавляются к заказу, 
    и общая стоимость заказа пересчитывается.

    Принимает: 
        request
    Возвращает: 
        Перенаправление на страницу со всеми заказами, если позиция успешно добавлена. 
        Перед добавлением позиции запрашивается подтверждение действия.

    :Raises: 
        Http404: отображение страницы 404, если заказа с указанным id не было найдено.
    """
    try:
        data: Orders = get_object_or_404(Orders, id=id)
    except Exception:
        raise Http404('Заказ с таким id не существует')
    
    if request.method == 'POST':
        with transaction.atomic(): 
            order_form = CreateOrderForm(request.POST, instance=data)

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

            return redirect(f'/edit-order/{int(id)}')
    else:
        order_form =CreateOrderForm(instance=data)
        meal_form = CreateMealForm()
        order_item_form = CreateOrderItemForm()
        context: dict = {
            'title': 'Добавление блюд',
            'order': data,
            'meal_form': meal_form,
            'order_item_form': order_item_form,
            'order_form': order_form
        }
            
        return render(request, 'add_items.html', context)
    

def page_not_found(request, exception) -> HttpResponseNotFound:
    """
    Осуществляет отображение страницы 404, если запрашиваемый URL не найден.

    Принимает: 
        request
        exception

    Возвращает 
        Страница 404
    """
    context: dict = {
        'exception': exception,
        'title': 'Страница не найдена',
    }
    return HttpResponseNotFound(render(request, '404.html', context))

