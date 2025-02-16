from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.show_orders, name='show_orders'),
    path('create-order/', views.create_order, name='create_order'),
    path('edit-status/<int:id>', views.edit_status, name='edit_status'),
    path('delete-order/<int:id>', views.delete_order, name='delete_order'),
]