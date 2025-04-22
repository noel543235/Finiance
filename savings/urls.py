from django.urls import path
from .views import *

app_name = 'savings'

urlpatterns = [
    path('', index, name="index"),
    path('create_goal', create_goal, name='create_goal'),
    path('update_goal', update_goal, name='update_goal'),
    path('update_retirement', update_retirement, name='update_retirement'),
    path('update_emergency', update_emergency, name='update_emergency'),
    path('get_chart_data', get_chart_data, name="get_chart_data"),
    path('create_category', create_category, name="create_category"),
    
]