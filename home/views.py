from django.shortcuts import render
from expenses.models import *
from savings.models import *
from itertools import chain

def index(request): 
    return render(request, "home/homepage.html", {})

def history(request): 
    savings_data = SavingsGoal.objects.all()
    
    # Change differently named date fields to 'display_date'
    def annotate(qs, date_field, type_name, amount_field='amount'):
        for obj in qs:
            setattr(obj, 'display_date', getattr(obj, date_field))
            setattr(obj, 'display_amount', getattr(obj, amount_field))
            setattr(obj, 'type', type_name)
        return qs

    one_time = annotate(OneTime.objects.all(), 'date_purchased', OneTime)
    recurring = annotate(
        Recurring.objects.exclude(pk__in=Loan.objects.values_list('pk', flat=True)),
        'start_date', "Recurring"
    )
    loan = annotate(Loan.objects.all(), 'start_date','Loan', 'principal')

    # Combine the three querysets
    expenses_data = list(chain(one_time, recurring, loan))
    return render(request, "home/history.html", {"savings_data": savings_data, "expenses_data": expenses_data})