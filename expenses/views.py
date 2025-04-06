from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from itertools import chain
from .forms import *
from .models import *
from datetime import datetime

def index(request):
    """Initial template when user visits expenses page

    Args:
        request (HttpRequest): User info

    Returns:
        HttpResponse: Template to load with context (forms, expenses, etc.)
    """
    
    # Redirects user to login page if they are not logged in
    if not request.user.is_authenticated:
        return redirect('/login/login')
    
    # Create context object to send to template
    context = index_context(request)
    
    return render(request, "expenses/expenses.html", context)


def index_context(request):
    # Query all user expenses from database
    onetime_expenses = OneTime.objects.filter(user=request.user)
    recurring_expenses = Recurring.objects.filter(user=request.user)
    
    # Create context object to send to template
    context = {
        "onetime_expenses": onetime_expenses,
        "recurring_expenses": recurring_expenses,
        "category_form": CategoryForm
    }
    
    return context
    

def add_expense(request):
    """Page where user creates expenses

    Args:
        request (HttpRequest): User info

    Returns:
        HttpResponse: Template to load with form
    """
    
    # Create context object containing expense form
    context = {
        "form": ExpenseForm
    }
    
    return render(request, "expenses/add_expense.html", context)


def create_expense(request):
    """View to process form and create expenses

    Args:
        request (HttpRequest): Form info

    Returns:
        HttpRedirect: Redirect to index page
    """
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
                    principal=form.cleaned_data['principal'],
                    apr=form.cleaned_data['apr'],
                    term_amt=form.cleaned_data['term_amt']
                )
                loan_expense.save()
                
    else:
        # Form is invalid, return the form with errors
        return render(request, 'expenses/add_expenses.html', {"form": form})
                

    return redirect("expenses:index")


def create_category(request):
    """View to process form and create categories

    Args:
        request (HttpRequest): Form info

    Returns:
        HttpRedirect: Redirect to index page
    """
    form = CategoryForm(request.POST)
    if form.is_valid():
        # Helper variable for cleaned form data
        f = form.cleaned_data
        
        category = Category(
            name=f['name']
        )
        category.save()
        
    else:
        # Form is invalid, return the form with errors
        context = index_context(request)
        context["category_form"] = form
        return render(request, 'expenses/expenses.html', context)
    
    return redirect("expenses:index")
        

def delete_onetime_expense(request, expense_id):
    """Deletes a one-time expense

    Args:
        request (HttpRequest): User info
        expense_id (int): PK identifying expense

    Returns:
        HttpRedirect: Redirect to index page
    """
    
    if not request.user.is_authenticated:
        return redirect('/login/login')
    
    expense = get_object_or_404(OneTime, pk=expense_id)

    if request.method == "POST":
            
        # Retrieve the expense, ensuring it belongs to the current user
        expense.delete()
            
            
    return redirect('expenses:index')


def delete_recurring_expense(request, expense_id):
    """Deletes a recurring expense

    Args:
        request (HttpRequest): User info
        expense_id (int): PK identifying expense

    Returns:
        HttpRedirect: Redirect to index page
    """
    
    if not request.user.is_authenticated:
        return redirect('/login/login')
    
    expense = get_object_or_404(Recurring, pk=expense_id)
    
    if request.method == "POST":
            
        # Retrieve the expense, ensuring it belongs to the current user
        expense.delete()
            
            
    return redirect('expenses:index')
    