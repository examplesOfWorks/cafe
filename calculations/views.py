from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Prefetch, Sum
from orders.models import Orders, OrderItems

def profit(request) -> HttpResponse:
    orders = Orders.objects.filter(status='Оплачено').prefetch_related(
        Prefetch(
            "orderitems_set",
            queryset=OrderItems.objects.select_related('meal')
        )
    )

    total_price = orders.aggregate(Sum('total_price')).get('total_price__sum')

    context: dict = {
        'orders': orders,
        'total_price': total_price,
        'title': 'Расчёт выручки'
    }
    return render(request, 'profit.html', context)
