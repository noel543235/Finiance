from django.shortcuts import render
from expenses.models import Expense
from django.db.models import Sum
from django.http import JsonResponse
from itertools import chain
from expenses.models import *
import json

def sum_expenses(expenses):
    total = 0
    for expense in expenses:
        total += expense.amount
        
    return total


def getUserExpenses(request):
    '''Return all expenses of the current user'''
    return list(chain(
        OneTime.objects.filter(user=request.user),
        Subscription.objects.filter(user=request.user),
        Loan.objects.filter(user=request.user)
    ))
    

def index(request):
    frequency = request.GET.get('frequency', 'Monthly')
    
    print(frequency)

    # Query the database for the top 10 Monthly expenses
    expenses = getUserExpenses(request)
    
    # Calculate the sum of all expenses 
    total = sum_expenses(expenses)
    
    # Calculate proportions for each expense relative to the total
    if total > 0:
        proportions = [float(expense.amount / total) for expense in expenses]
    else:
        proportions = [0] * len(expenses)
    
    return render(request, "savings/savings.html", {'expenses': expenses, 'proportions': proportions})
    
def get_expenses(request):
    frequency = request.GET.get('frequency', 'Monthly') 

    # Query the database for all expenses
    expenses = list(chain(
        OneTime.objects.filter(user=request.user),
        Subscription.objects.filter(user=request.user),
        Loan.objects.filter(user=request.user)
    ))
    
    # Sort expenses by date
    expenses = sorted(expenses, key = lambda x: x.date, reverse=True)   
    
    # Calculate the sum of all expenses 
    total = sum_expenses(expenses)

    # Calculate proportions for each expense relative to the total
    if total > 0:
        proportions = [expense.amount / total for expense in expenses]
    else:
        proportions = [0] * len(expenses)
    
    expenses_data = list(expenses.values('label', 'amount'))

    # Convert to JSON format
    return JsonResponse({'expenses': expenses_data, 'proportions': proportions})

def future_value_calculator(present_value, compounds, interest_rate, periodic_deposit):
    '''
    Parameters: float: present_value, int: compounds, int: interest rate,
        float: periodic deposit

    Returns: 2D list: compounds_rows

    this method calculates the future value and displays the stats for each
    compound
    '''
    # initialize 2D list: compound_rows and change the interest rate to decimal form
    compound_rows = []
    interest_rate = interest_rate/100

    # loop through the number of compounds
    for i in range(compounds):
        
        # calculate the future value for each compound and add the present value,
        # deposit amount, interest of present value, and the future value
        future_value = present_value * (1 + interest_rate) + periodic_deposit
        compound_rows.append([present_value, periodic_deposit, interest_rate*present_value, future_value])

        # set the new present value for the next iteration
        present_value = future_value

    return compound_rows
