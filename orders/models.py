from django.db import models

class Meals(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название блюда')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена') 

    class Meta:
        db_table = 'meal'
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ("id",)

    def __str__(self):
        return f"Название: {self.name} | Цена: {self.price}"
   
        
class Orders(models.Model):
    table_number = models.IntegerField(verbose_name='Номер стола')
    total_price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Общая цена')
    status = models.CharField(max_length=100, verbose_name='Статус')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ("id",)

    def __str__(self):
        return f"Заказ № {self.pk} | Стол: {self.table_number} | Сумма: {self.total_price} | Статус: {self.status} | Дата: {self.created_timestamp}"

class OrderItems(models.Model):
    order = models.ForeignKey(to=Orders, on_delete=models.CASCADE, verbose_name='Заказ')
    meal = models.ForeignKey(to=Meals, on_delete=models.CASCADE, verbose_name='Блюдо')
    quantity = models.IntegerField(verbose_name='Количество')
    item_price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена позиции')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
        ordering = ("id",)

    def __str__(self):
        return f"Заказ № {self.order} | Блюдо: {self.meal} | Количество: {self.quantity} | Цена позиции: {self.item_price}"
