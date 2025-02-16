from django.db.models import Prefetch
from orders.models import Orders, OrderItems
from django.db.models import Q

def q_search(query):
    if query.isdigit() and len(query) <= 2:
        return Orders.objects.filter(table_number=int(query)).prefetch_related(
            Prefetch(
                "orderitems_set",
                queryset=OrderItems.objects.select_related('meal')
            )
        )
    return Orders.objects.filter(status__icontains=query)

def filter_by_status(waiting, ready, paid):
    q_objects = Q()

    if waiting:
        q_objects |= Q(status='В ожидании')
    if ready:
        q_objects |= Q(status='Готово')
    if paid:
        q_objects |= Q(status='Оплачено')

    return Orders.objects.filter(q_objects).prefetch_related(
        Prefetch(
            "orderitems_set",
            queryset=OrderItems.objects.select_related('meal')
        )
    )