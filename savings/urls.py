from django.urls import path
from .views import *

app_name = 'savings'

urlpatterns = [
    path('', index, name="index"),
    path('create_goal', create_goal, name='create_goal'),
    path('get_chart_data', get_chart_data, name="get_chart_data"),
    path('calculate', calculate, name="calculate"),
    path('create_category', create_category, name="create_category"),
    
]