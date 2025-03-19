from django import forms
from django.forms import Form, ModelForm
from .models import *      

class SavingsGoalForm(ModelForm):
    
    class Meta:
        model = SavingsGoal
        fields = ['label', 'amount', 'start_date', 'frequency', 'next_due_date', 'end_date', 'category']        
        
class LoanPaymentForm(ModelForm):
    
    class Meta:
        model = GoalPayment
        fields = ['goal', 'payment_date', 'amount']