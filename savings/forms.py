from django import forms
from django.forms import Form
from .models import *   
from expenses.models import Category   

class SavingsGoalForm(Form):
    label = forms.CharField(max_length=50, label='Goal Name')
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Goal Amount')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Description')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category')
    initial = forms.DecimalField(decimal_places=2, label='Amount Saved So Far')
        
class GoalPaymentForm(Form):
    goal = forms.ModelChoiceField(queryset=SavingsGoal.objects.all(), label='Please Select Goal')
    payment_date = forms.DateField(label='Payment Date')
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Payment Amount')
