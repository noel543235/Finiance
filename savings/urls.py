from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('create_goal', create_goal, name='create_goal'),
    path('get_chart_data', get_chart_data, name="get_chart_data"),
]