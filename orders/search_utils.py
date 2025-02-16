from django.db.models import Prefetch
from orders.models import Orders, OrderItems

def q_search(query):
    if query.isdigit() and len(query) <= 2:
        return Orders.objects.filter(table_number=int(query)).prefetch_related(
            Prefetch(
                "orderitems_set",
                queryset=OrderItems.objects.select_related('meal')
            )
        )
    return Orders.objects.filter(status__icontains=query)