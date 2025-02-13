from django.urls import path
from .views import index, get_expenses

urlpatterns = [
    path('', index, name="index"),
    path('get_expenses', get_expenses, name="get_expenses"),  # AJAX request handler
]