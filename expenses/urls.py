from django.urls import path
from .views import add_expense, expense_list

from . import views

urlpatterns = [
    path("add/", add_expense, name="add_expense"),
    path("",expense_list, name="expenses"),
]