from django import forms
from django.forms import Form, ModelForm
from .models import *

class ExpenseForm(Form):
    
    EXPENSE_CHOICES = [
        ('O', 'One Time'),
        ('S', 'Subscription'),
        ('L', 'Loan')
    ]
    
    expense_type = forms.ChoiceField(choices = EXPENSE_CHOICES)


class OneTimeForm(ModelForm):
    
    class Meta:
        model = OneTime
        fields = ['label', 'amount', 'category']
        

class SubscriptionForm(ModelForm):
    
    class Meta:
        model = Subscription
        fields = ['label', 'amount', 'category', 'frequency']
        

class LoanForm(ModelForm):
    
    class Meta:
        model = Loan
        fields = ['label', 'amount', 'category', 'interest_rate']