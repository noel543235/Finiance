from django.shortcuts import render, redirect
from django.http import JsonResponse
from itertools import chain
from expenses.models import *
from .forms import *
from django.test import TestCase, SimpleTestCase
import json
from datetime import datetime


def index(request):
    """Initial template when user visits savings page

    Args:
        request (HttpRequest): User info

    Returns:
        HttpResponse: Template to load with context (forms, goals, etc.)
    """
    context = index_context(request)
    
    return render(request, "savings/savings.html", context)


def index_context(request):
    # Query all user goals from the database
    goals = getUserGoals(request)
    
    # Create context object to send to template
    context = {
        'goals': goals,
        'goal_form': SavingsGoalForm,
        'payment_form': GoalPaymentForm
    }
    
    return context
    
   

def getUserGoals(request):
    """Return all savings goals of the current user

    Args:
        request (HttpRequest): User info

    Returns:
        iterable: Iterable of savings goal objects
    """
    return SavingsGoal.objects.filter(user=request.user)


def getGoalPayments(goal):
    """Get a list of all goal payments for the current user

    Args:
        goal (models.SavingsGoal): Saving's goal of current user

    Returns:
        iterable: All payment objects linked to given savings goal object
    """
    return goal.goalpayment_set.all()


def getGoalPercentages(goals):
    """Calculate the percetage reached for each given goal

    Args:
        goals (models.SavingsGoal): Iterable of savings goal objects

    Returns:
        arr[float]: Percent completed for each goal
    """
    # Initialize percentages array
    percentages = list()
    
    # Calculate goal % reached for every goal
    for goal in goals:
        payments = getGoalPayments(goal) # Get all payments for specific goal
        total = sum(payment.amount for payment in payments) # Sum payments 
        percent = max(0.01, total / goal.amount) # Convert to percent (showing 0% as 0.1%)
        percentages.append(percent * 100)
        
    return percentages 


def create_goal(request): 
    """View to process form and create goal

    Args:
        request (HttpRequest): Form info

    Returns:
        HttpRedirect: Redirect to index page
    """
    form = SavingsGoalForm(request.POST)
    if form.is_valid():
        # Helper variable for cleaned form
        f = form.cleaned_data
        
        # Handle one-time expense
        savings_goal = SavingsGoal(
            # Mandatory fields
            user=request.user,
            label=f['label'],
            amount=f['amount'],
            frequency=f['frequency'],
            payment_amount=f['payment_amount'],
            start_date=f['start_date'],
            category=f['category'],
            date_created=datetime.now(),
            )
        savings_goal.save()
        
        # Make initial payment towards goal
        initial = f['initial']
        payment = GoalPayment(
            goal=savings_goal,
            payment_date=datetime.now(),
            amount=initial            
        )
        payment.save()
        
    else:
        # Form is invalid, return the form with errors
        context = index_context(request)
        context['goal_form'] = form
        return render(request, 'savings/savings.html', context)
        
    return redirect('savings:index')
    
    
    
def get_chart_data(request):
    """Get up-to-date goal info for goals bar chart

    Args:
        request (HttpRequest): User info

    Returns:
        json: Goal labels and their percentages reached
    """
    # Query the database for all expenses
    goals = getUserGoals(request) 
    
    # Calculate percentages reached per goal    
    proportions = getGoalPercentages(goals)
    
    # Labels for each goal
    labels = [goal.label for goal in goals]
    
    # print(labels, proportions)

    # Convert to JSON format
    return JsonResponse({'labels': labels, 'data': proportions})


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
    print("calculates!!!")
    # loop through the number of compounds
    for i in range(compounds):
        
        # calculate the future value for each compound and add the present value,
        # deposit amount, interest of present value, and the future value
        future_value = present_value * (1 + interest_rate) + periodic_deposit
        compound_rows.append([str(i+1), "${:.2f}".format(present_value), "${:.2f}   ".format(periodic_deposit),
                                "${:.2f}".format(interest_rate*present_value), "${:.2f}".format(future_value)])

        # set the new present value for the next iteration
        present_value = future_value

    return compound_rows

def calculate(request):
    print("Calculate")
    if request.method == "POST":
        present_value = request.POST.get("present_value")
        compounds = request.POST.get("compounds")
        periodic_deposit = request.POST.get("periodic_deposit")
        interest_rate = request.POST.get("interest_rate")
        print(f"present value = {present_value} compounds = {compounds} periodic deposit = {periodic_deposit} interest rate = {interest_rate}")
        
        table = future_value_calculator(float(present_value), int(compounds), float(interest_rate), float(periodic_deposit))
        print(table)
        
        return render(request, "savings/savings.html", {"table": table})
    
    
    return render(request, "savings/savings.html")