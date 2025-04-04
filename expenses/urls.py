from django.urls import path
from .views import *

urlpatterns = [
    path("add/", add_expense, name="add_expense"),
    path("",expense_list, name="expenses"),
    path('delete/onetime/<int:expense_id>/', delete_onetime_expense, name='delete_onetime_expense'),
    path('delete/recurring/<int:expense_id>/', delete_recurring_expense, name='delete_recurring_expense'),
    path('import/', import_expenses, name='import_expenses'),
    path('import_data/', import_data, name='import_data'),
    path('import_data/import_result/', import_result, name='import_result'),
]