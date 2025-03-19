from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from itertools import chain
from .forms import *
from .models import *
from datetime import datetime

def add_expense(request):
    """Handles adding a new expense for the logged-in user."""

    # Redirects user to login page if they are not logged in
    if not request.user.is_authenticated:
        return redirect('/login/login')

    # Initialize general form allowing user to select one-time or recurring expense
    form = ExpenseForm()

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            is_recurring = form.cleaned_data['is_recurring']
            is_loan = form.cleaned_data['is_loan']

            if not is_recurring:
                # Handle one-time expense
                one_time_expense = OneTime(
                    user=request.user,
                    label=form.cleaned_data['label'],
                    amount=form.cleaned_data['amount'],
                    description=form.cleaned_data['description'],
                    category=form.cleaned_data['category'],
                    date_created=datetime.now(),
                    date_purchased=form.cleaned_data['date_purchased']
                )
                one_time_expense.save()
            else:
                if not is_loan:
                    # Handle recurring expense
                    recurring_expense = Recurring(
                        user=request.user,
                        label=form.cleaned_data['label'],
                        amount=form.cleaned_data['amount'],
                        description=form.cleaned_data['description'],
                        category=form.cleaned_data['category'],
                        date_created=datetime.now(),
                        start_date=form.cleaned_data['start_date'],
                        end_date=form.cleaned_data['end_date'],
                        frequency=form.cleaned_data['frequency'],
                        next_due_date=form.cleaned_data['next_due_date']
                    )
                    recurring_expense.save()
                
                else:
                    # Handle loan expense
                    loan_expense = Loan(
                        user=request.user,
                        label=form.cleaned_data['label'],
                        amount=form.cleaned_data['amount'],
                        description=form.cleaned_data['description'],
                        category=form.cleaned_data['category'],
                        date_created=datetime.now(),
                        start_date=form.cleaned_data['start_date'],
                        end_date=form.cleaned_data['end_date'],
                        frequency=form.cleaned_data['frequency'],
                        next_due_date=form.cleaned_data['next_due_date'],
                        principal=form.cleaned_data['principal'],
                        apr=form.cleaned_data['apr'],
                        term_amt=form.cleaned_data['term_amt']
                    )
                    loan_expense.save()
                    

    return render(request, "expenses/add_expense.html", {'form': form})


def expense_list(request):
    """Displays a list of expenses for the logged-in user, sorted by date."""

    if not request.user.is_authenticated:
        return redirect('/login/login')

    onetime_expenses = OneTime.objects.filter(user=request.user)
    recurring_expenses = Recurring.objects.filter(user=request.user)
    
    return render(request, "expenses/expenses.html", {"onetime_expenses": onetime_expenses, "recurring_expenses": recurring_expenses})

def delete_onetime_expense(request, expense_id):
    """Deletes an expense if it belongs to the logged-in user."""
    
    if not request.user.is_authenticated:
        return redirect('/login/login')
    
    expense = get_object_or_404(OneTime, pk=expense_id)

    if request.method == "POST":
            
        # Retrieve the expense, ensuring it belongs to the current user
        expense.delete()

        # expense.delete()
            
            
    return redirect('expenses')


def delete_recurring_expense(request, expense_id):
    """Deletes an expense if it belongs to the logged-in user."""
    
    if not request.user.is_authenticated:
        return redirect('/login/login')
    
    expense = get_object_or_404(Recurring, pk=expense_id)
    
    if request.method == "POST":
            
        # Retrieve the expense, ensuring it belongs to the current user
        expense.delete()
        
        # expense.delete()
            
            
    return redirect('expenses')