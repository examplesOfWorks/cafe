from django import forms
from orders.models import Orders, Meals, OrderItems

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['table_number']

    table_number = forms.IntegerField(
        label='Номер стола',
        widget=forms.NumberInput(attrs={
            'min': 1, 
            'max': 10, 
            'class': 'form-control',
            'placeholder': 'Введите номер стола',
            'required': 'required',
            }
        )
    )

class CreateOrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItems
        fields = ['quantity']

    quantity = forms.IntegerField(
        label='Количество, шт.',
        widget=forms.NumberInput(attrs={
            'min': 1, 
            'class': 'form-control', 
            'placeholder': 'Сколько этого блюда заказать?',
            'required': 'required',
            }
        )
    )

class CreateMealForm(forms.ModelForm):
    class Meta:
        model = Meals
        fields = ['name', 'price']
    name = forms.CharField(
        label='Название блюда',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Введите название блюда',
            'required': 'required',
        }))
    price = forms.DecimalField(
        label='Цена, руб.',
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Введите цену блюда',
            'required': 'required',
        })
        )



