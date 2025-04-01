from django.urls import path
from .views import *

urlpatterns = [
    path("add/", add_expense, name="add_expense"),
    path("",expense_list, name="expenses"),
    path('delete/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('load-expense-form/', load_expense_form, name='load_expense_form'),
    path('import/', import_expenses, name='import_expenses'),
    path('import_data/', import_data, name='import_data'),
    path('import_data/import_result/', import_result, name='import_result'),
]