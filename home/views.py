from django.shortcuts import render
from expenses.models import *
from savings.models import *
from itertools import chain
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from savings.views import get_payments


def index(request): 
    return render(request, "home/homepage.html", {})

def history(request): 
    savings_data = get_payments(request, SavingsGoal.objects.filter(user=request.user))
    
    # Change differently named date fields to 'display_date'
    def annotate(qs, date_field, type_name, amount_field='amount'):
        for obj in qs:
            setattr(obj, 'display_date', getattr(obj, date_field))
            setattr(obj, 'display_amount', getattr(obj, amount_field))
            setattr(obj, 'type', type_name)
        return qs

    one_time = annotate(OneTime.objects.filter(user=request.user), 'start_date', 'One-Time')
    recurring = annotate(
        get_recent_recurring(request),
        'start_date', "Recurring"
    )
    loan = annotate(get_recent_loans(request), 'start_date','Loan', 'amount')

    # Combine the three querysets
    expenses_data = sorted(list(chain(one_time, recurring, loan)), key=lambda x: x.start_date, reverse=True)
    return render(request, "home/history.html", {"savings_data": savings_data, "expenses_data": expenses_data})


def get_recent_recurring(request):
    today = datetime.today().date()
    months2_ago = today-relativedelta(months=2)

    recurring_expenses = list()
    
    for expense in Recurring.objects.filter(user=request.user).exclude(pk__in=Loan.objects.values_list('pk', flat=True)):
        payment_date = expense.start_date
        while payment_date <= today and ((expense.end_date is None) or expense.end_date >= today):
            if payment_date >= months2_ago:
                recurring_expenses.append(copy_expense(expense, payment_date))
            payment_date = expense.when_next_payment(payment_date)  
                
    return sorted(recurring_expenses, key=lambda x: x.start_date, reverse=True)

def get_recent_loans(request):
    today = datetime.today().date()
    months2_ago = today-relativedelta(months=2)

    recurring_expenses = list()
    
    for expense in Loan.objects.filter(user=request.user):
        payment_date = expense.start_date
        while payment_date <= today and ((expense.end_date is None) or expense.end_date >= today):
            if payment_date >= months2_ago:
                recurring_expenses.append(copy_expense(expense, payment_date))
            payment_date = expense.when_next_payment(payment_date)  
                
    return sorted(recurring_expenses, key=lambda x: x.start_date, reverse=True)


def copy_expense(orig, day):
    new = Recurring()
    for field in orig._meta.fields:
        setattr(new, field.name, getattr(orig, field.name))
        
    new.start_date = day
        
    return new