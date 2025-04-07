from django import forms
from django.forms import Form, ModelForm
from expenses.models import Recurring
from .models import SavingsAccount, SavingsGoal

class FrequencyForm(Form):
      
    frequency = forms.ChoiceField(choices = Recurring.FREQUENCY_CHOICES)


class SavingsAccountForm(ModelForm):
    
    class Meta:
        model = SavingsAccount
        fields = ['label', 'amount', 'category']
        

class SavingsGoalForm(ModelForm):
    
    class Meta:
        model = SavingsGoal
        fields = ['label', 'amount', 'start_date', 'frequency', 'next_due_date', 'end_date', 'category']        
        
class LoanPaymentForm(ModelForm):
    
    class Meta:
        model = GoalPayment
        fields = ['goal', 'payment_date', 'amount']