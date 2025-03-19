from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from itertools import chain
from .forms import *
from .models import *

def add_expense(request):
    """Handles adding a new expense for the logged-in user."""

    # Redirects user to login page if they are not logged in
    if not request.user.is_authenticated:
        return redirect('/login/login')

    # Initialize
    form = GeneralForm(request.POST)

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense_type = form.cleaned_data["expense_type"]
            selected_expense_type = expense_type

            # Determine the correct form to use based on selected expense type
            if expense_type == 'O':
                expense_form = OneTimeForm(request.POST)
            elif expense_type == 'S':
                expense_form = SubscriptionForm(request.POST)
            elif expense_type == 'L':
                expense_form = LoanForm(request.POST)
            
            if expense_form and expense_form.is_valid():
                expense = expense_form.save(commit=False)
                expense.user = request.user  # Associate expense with the logged-in user
                expense.save()
                return redirect("expenses")

    else:  # Handle GET request
        form = ExpenseForm()
        selected_expense_type = request.GET.get('expense_type', None)

    return render(request, "expenses/add_expense.html", {
        "form": form,
        "expense_form": expense_form,
        "selected_expense_type": selected_expense_type
    })

def load_expense_form(request):
    """Loads the specific form based on the selected expense type."""
    expense_type = request.GET.get('expense_type')

    # Handle form creation based on expense_type
    if expense_type == 'O':
        form = OneTimeForm()
    elif expense_type == 'S':
        form = SubscriptionForm()
    elif expense_type == 'L':
        form = LoanForm()
    else:
        form = None

    # If form is valid, return the form HTML rendered as a string
    if form:
        form_html = form.as_p()
        return JsonResponse({"form_html": form_html})
    else:
        return JsonResponse({"form_html": ""}, status=400)


def expense_list(request):
    """Displays a list of expenses for the logged-in user, sorted by date."""

    if not request.user.is_authenticated:
        return redirect('/login/login')

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
