from django.urls import path

from calculations import views

app_name = 'calculations'

urlpatterns: list = [
    path('profit/', views.profit, name='profit'),
]