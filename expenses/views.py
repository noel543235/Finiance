from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm
from .models import Expense


def add_expense(request):
    """Handles adding a new expense for the logged-in user."""

    if not request.user.is_authenticated:
        return redirect('/login/login')

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)  # Create an expense instance without saving yet
            expense.user = request.user        # Associate the expense with the logged-in user
            expense.save()                     # Save the expense to the database
            return redirect("expenses")
    else:
        form = ExpenseForm()
    return render(request, "expenses/add_expense.html", {"form": form})


def expense_list(request):
    """Displays a list of expenses for the logged-in user, sorted by date."""

    if not request.user.is_authenticated:
        return redirect('/login/login')

    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, "expenses/expenses.html", {"expenses": expenses})


def delete_expense(request, expense_id):
    """Deletes an expense if it belongs to the logged-in user."""

    if not request.user.is_authenticated:
        return redirect('/login/login')

    if request.method == "POST":

        # Retrieve the expense, ensuring it belongs to the current user
        expense = get_object_or_404(Expense, id=expense_id, user=request.user) 
        expense.delete()
    return redirect('expenses')
