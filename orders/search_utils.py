from django.db.models import Prefetch
from django.db.models import Q
from orders.models import Orders, OrderItems

def q_search(query):
    """
    Поиск заказов по запросу из поисковой строки. Значение из запроса может быть числом (номер стола)
    или строкой (статус заказа).

    Принимает: 
        Данные для поиска.

    Возвращает:
        Список заказов со соответствующими статусами или номером стола.
    """
    if query.isdigit() and len(query) <= 2:
        return Orders.objects.filter(table_number=int(query)).prefetch_related(
            Prefetch(
                "orderitems_set",
                queryset=OrderItems.objects.select_related('meal')
            )
        )
    return Orders.objects.filter(status__icontains=query)

def filter_by_status(waiting, ready, paid):
    """
    Фильтрует заказы по выбранным статусам.

    Принимает:
        waiting - флаг, фильтровать ли заказы со статусом 'В ожидании'
        ready - флаг, фильтровать ли заказы со статусом 'Готово'
        paid - флаг, фильтровать ли заказы со статусом 'Оплачено'

    Возвращает:
        Список заказов, соответствующих выбранным статусам.
    """
    # создаём фильтр по выбранным статусам используя оператор "|", чтобы можно было выбрать несколько статусов
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