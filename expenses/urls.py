from django.urls import path
from .views import *

app_name = 'expenses'

urlpatterns = [
    path("add/", add_expense, name="add_expense"),
    path("", index, name="index"),
    path("create_expense", create_expense, name="create_expense"),
    path("create_category", create_category, name="create_category"),
    path('delete/onetime/<int:expense_id>/', delete_onetime_expense, name='delete_onetime_expense'),
    path('delete/recurring/<int:expense_id>/', delete_recurring_expense, name='delete_recurring_expense'),
]