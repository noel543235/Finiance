from django import forms
from django.forms import Form, ModelForm
from expenses.models import FREQUENCY_CHOICES
from .models import SavingsAccount, SavingsGoal

class FrequencyForm(Form):
      
    frequency = forms.ChoiceField(choices = FREQUENCY_CHOICES)


class SavingsAccountForm(ModelForm):
    
    class Meta:
        model = SavingsAccount
        fields = ['label', 'amount', 'category']
        

class SavingsGoalForm(ModelForm):
    
    class Meta:
        model = SavingsGoal
        fields = ['label', 'amount', 'category', 'frequency']