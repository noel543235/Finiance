from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from itertools import chain
from .forms import ExpenseForm, OneTimeForm, SubscriptionForm, LoanForm
from .models import OneTime, Subscription, Loan, Expense

def add_expense(request):
    """Handles adding a new expense for the logged-in user."""

    if not request.user.is_authenticated:
        return redirect('/login/login')

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense_type = form.cleaned_data["expense_type"]

            # Determine the correct form to use
            if expense_type == 'O':
                expense_form = OneTimeForm(request.POST)
            elif expense_type == 'S':
                expense_form = SubscriptionForm(request.POST)
            elif expense_type == 'L':
                expense_form = LoanForm(request.POST)
            else:
                expense_form = None

            if expense_form and expense_form.is_valid():
                expense = expense_form.save(commit=False)
                expense.user = request.user  # Associate expense with the logged-in user
                expense.save()
                return redirect("expenses")

    else:
        form = ExpenseForm()
        expense_form = None

    return render(request, "expenses/add_expense.html", {"form": form, "expense_form": expense_form})


def expense_list(request):
    """Displays a list of expenses for the logged-in user, sorted by date."""
    expenses = chain(
        OneTime.objects.filter(user=request.user),
        Subscription.objects.filter(user=request.user),
        Loan.objects.filter(user=request.user)
    )
    
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
