from django import forms
from django.forms import Form
from .models import *
from expenses.models import Category, Recurring 

class SavingsGoalForm(Form):
    label = forms.CharField(max_length=50)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    frequency = forms.ChoiceField(choices=Recurring.FREQUENCY_CHOICES)
    payment_amount = forms.DecimalField(max_digits=10, decimal_places=2)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    initial = forms.DecimalField(decimal_places=2)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    
    
class UpdateSavingsForm(Form):
    label = forms.ModelChoiceField(queryset=SavingsGoal.objects.none())
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    payment_amount = forms.DecimalField(max_digits=10, decimal_places=2)
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only update the queryset for the specific field
        self.fields['label'].queryset = SavingsGoal.objects.filter(user=user)
        
class GoalPaymentForm(Form):
    goal = forms.ModelChoiceField(queryset=SavingsGoal.objects.all())
    payment_date = forms.DateField()
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    
    
class UpdateRetirement(Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    
class UpdateEmergency(Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
