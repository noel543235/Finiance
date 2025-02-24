from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['label', 'amount', 'frequency']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Label'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            'frequency': forms.Select(choices=Expense.FREQUENCY_CHOICES, attrs={'class': 'form-select', 'aria-label': 'Default'})  # Dropdown for frequency
        }
    