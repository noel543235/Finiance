from django.urls import path
from .views import add_expense, expense_list, delete_expense, load_expense_form

urlpatterns = [
    path("add/", add_expense, name="add_expense"),
    path("",expense_list, name="expenses"),
    path('delete/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('load-expense-form/', load_expense_form, name='load_expense_form'),
]