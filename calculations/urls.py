from django.urls import path

from calculations import views

app_name = 'calculations'

urlpatterns = [
    path('profit/', views.profit, name='profit'),
]