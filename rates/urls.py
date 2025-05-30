from django.urls import path
from .views import currency_rates

urlpatterns = [
    path('', currency_rates, name='currency_rates'),
]
