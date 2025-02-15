from django.shortcuts import render

def show_orders(request):
    context = {
        'title': 'Все заказы',
    }
    
    return render(request, 'index.html', context)

def create_order(request):
    context = {
        'title': 'Создание заказа',
    }
    
    return render(request, 'create.html', context)

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