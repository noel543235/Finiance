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