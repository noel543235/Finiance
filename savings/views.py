from django.shortcuts import render
from django.http import JsonResponse
from itertools import chain
from expenses.models import *
from .forms import *
from django.test import TestCase, SimpleTestCase
import json


def sumExpenses(expenses):
    '''Sum amounts of given expenses'''
    total = 0
    for expense in expenses:
        total += expense.amount
        
    return total


def getProportions(expenses):
    '''Calculate the proportions of each expense amount relative to the total'''
    # Find total of all expenses
    total = sumExpenses(expenses)
    
    # Calculate proportions
    if total > 0:
        proportions = [float(expense.amount / total) for expense in expenses]
    else:
        proportions = [0]
        
    return proportions


def getUserExpenses(request):
    '''Return all expenses of the current user'''
    return list(chain(
        OneTime.objects.filter(user=request.user),
        Recurring.objects.filter(user=request.user),
    ))  
    

def getUserGoals(request):
    '''Return all savings goals of the current user''' 
    return SavingsGoal.objects.filter(user=request.user)


def getGoalPayments(goal):
    return goal.goalpayment_set.all()


def getGoalProportions(goals):
    '''Calculate the percetage completed for each goal'''
    proportions = list()
    for goal in goals:
        payments = getGoalPayments(goal)
        total = sum(payment.amount for payment in payments)
        percent = max(0.01, total / goal.goal_amount)
        proportions.append(percent * 100)
        
    return proportions
        
    

def index(request):
    '''Initial template when user visits page'''
    # Query all user expenses from the database
    goals = getUserGoals(request)       
    
    return render(request, "savings/savings.html", {'expenses': goals})
    
def get_chart_data(request):
    frequency = request.GET.get('frequency')

    # Query the database for all expenses
    goals = getUserGoals(request) 
    
    proportions = getGoalProportions(goals)
    
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
    # loop through the number of compounds
    for i in range(compounds):
        
        # calculate the future value for each compound and add the present value,
        # deposit amount, interest of present value, and the future value
        future_value = present_value * (1 + interest_rate) + periodic_deposit
        compound_rows.append([str(i+1), "${:.2f}".format(present_value), "${:.2f}".format(periodic_deposit),
                                "${:.2f}".format(interest_rate*present_value), "${:.2f}".format(future_value)])

        # set the new present value for the next iteration
        present_value = future_value

    return compound_rows

def calculate(request):
    if request.method == "POST":
        present_value = request.POST.get("present_value")
        compounds = request.POST.get("compounds")
        periodic_deposit = request.POST.get("periodic_deposit")
        interest_rate = request.POST.get("interest_rate")
        
        table = future_value_calculator(float(present_value), int(compounds), float(interest_rate), float(periodic_deposit))
        
        return render(request, "savings/savings.html", {"table": table})
    
    return render(request, "savings/savings.html")


