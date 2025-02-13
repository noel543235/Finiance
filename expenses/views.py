from django.shortcuts import render, redirect
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