from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('get_chart_data/', get_chart_data, name="get_chart_data"),
    path('calculate/', calculate, name="calculate")
]