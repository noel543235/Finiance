from django import forms
from django.forms import Form, ModelForm
from .models import *      

class SavingsGoalForm(ModelForm):
    
    class Meta:
        model = SavingsGoal
        fields = ['label', 'goal_amount', 'amount', 'start_date', 'frequency', 'category']        
        
class LoanPaymentForm(ModelForm):
    
    class Meta:
        model = GoalPayment
        fields = ['goal', 'payment_date', 'amount']