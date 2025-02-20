from django.shortcuts import render
from expenses.models import Expense
from django.db.models import Sum
from django.http import JsonResponse
import json


def index(request):

    frequency = "Monthly"

    # Query the database for the top 10 Monthly expenses
    expenses = Expense.objects.filter(frequency=frequency).order_by('-amount')[:10]
    
    # Calculate the sum of all Monthly expenses 
    total_expenses = Expense.objects.filter(frequency=frequency).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate proportions for each expense relative to the total
    proportions = [expense.amount/total_expenses * 360 if total_expenses > 0 else 0 for expense in expenses]
    proportions = [float(proportion) for proportion in proportions]
    return render(request, "savings/savings.html", {'expenses':expenses, 'proportions': json.dumps(proportions)})
    
def get_expenses(request):
    frequency = request.GET.get('frequency', 'Monthly') 

    # Query the database for the top 10 expenses for that frequency
    expenses = Expense.objects.filter(frequency=frequency).order_by('-amount')[:10]
    
    # Calculate total expenses sum
    total_expenses = Expense.objects.filter(frequency=frequency).aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate proportions for chart
    proportions = [expense.amount / total_expenses * 360 if total_expenses > 0 else 0 for expense in expenses]
    proportions = [float(proportion) for proportion in proportions]
    
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
