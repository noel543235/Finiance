from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm
from .models import Expense


def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect("expenses")
    else:
        form = ExpenseForm()

    return render(request, "expenses/add_expense.html", {"form": form})


def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, "expenses/expenses.html", {"expenses": expenses})


def delete_expense(request, expense_id):
    if request.method == "POST":
        expense = get_object_or_404(Expense, id=expense_id)
        expense.delete()
    return redirect('expenses')
