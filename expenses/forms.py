from django import forms
from django.forms import Form
from .models import *


class ExpenseForm(Form):
    label = forms.CharField(max_length=50, label='Expense name')
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Amount')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Description')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category')
    is_recurring = forms.BooleanField(required=False, label='Is the expense recurring?')
    
    # Dynamic fields for One Time Expense
    date_purchased = forms.DateField(widget=forms.SelectDateWidget(), required=False, label='Date purchased')
    
    # Dynamic fields for Recurring Expense
    start_date = forms.DateField(widget=forms.SelectDateWidget(), required=False, label='Start date')
    end_date = forms.DateField(widget=forms.SelectDateWidget(), required=False, label='End date (optional)')
    frequency = forms.ChoiceField(choices=Recurring.FREQUENCY_CHOICES, required=False, label='How often does the expense occur?')
    is_loan = forms.BooleanField(required=False, initial=False, label='Does the expense accrue interest?')
    
    # Dynamic fields for Loan
    principal = forms.DecimalField(max_digits=20, decimal_places=2, required=False, label='Loan principal')
    apr = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Annual percentage rate')
    term_amt = forms.IntegerField(required=False, label='Term length (months)') 
  
    
'''
class GeneralForm(Form):
    
    is_recurring = forms.BooleanField()
    is_loan = forms.BooleanField()


class OneTimeForm(ModelForm):
    
    class Meta:
        model = OneTime
        fields = ['label', 'amount', 'date_purchased', 'category', 'description']
        

class RecurringForm(ModelForm):
    
    class Meta:
        model = Recurring
        fields = ['label', 'amount', 'start_date', 'frequency', 'next_due_date', 'end_date', 'category']
        

class LoanForm(ModelForm):
    
    class Meta:
        model = Loan
        fields = ['label', 'principal', 'amount', 'apr', 'term_amt', 'frequency', 'start_date', 'next_due_date', 'category']
        
        
class LoanPaymentForm(ModelForm):
    
    class Meta:
        model = LoanPayment
        fields = ['loan', 'payment_date', 'amount']
'''