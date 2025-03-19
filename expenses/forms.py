from django import forms
from django.forms import Form, ModelForm
from .models import *

class GeneralForm(Form):
    
    is_recurring = forms.BooleanField()


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