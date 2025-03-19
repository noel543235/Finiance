from django.urls import path
from .views import *

urlpatterns = [
    path("add/", add_expense, name="add_expense"),
    path("", expense_list, name="expenses"),
    path('delete/onetime/<int:expense_id>/', delete_onetime_expense, name='delete_onetime_expense'),
    path('delete/recurring/<int:expense_id>/', delete_recurring_expense, name='delete_recurring_expense'),
]