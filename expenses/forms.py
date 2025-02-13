from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['label', 'amount', 'frequency']
        widgets = {
            'frequency': forms.Select(choices=Expense.FREQUENCY_CHOICES)  # Dropdown for frequency
        }
    