from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.show_orders, name='show_orders'),
    path('create-order/', views.create_order, name='create_order'),
    path('edit-status/<int:id>', views.edit_status, name='edit_status'),
    path('edit-order/<int:id>', views.edit_order, name='edit_order'),
    path('delete-item/<int:id>', views.delete_item, name='delete_item'),
    path('add-items/<int:id>', views.add_items, name='add_items'),
    path('delete-order/<int:id>', views.delete_order, name='delete_order'),
]