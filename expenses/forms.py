from django import forms
from django.forms import Form
from .models import *


class ExpenseForm(Form):
    label = forms.CharField(
        max_length=50
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    description = forms.CharField(
        widget=forms.Textarea, required=False
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False
    )
    is_recurring = forms.BooleanField(
        required=False
    )
    
    # Dynamic fields for One Time Expense
    date_purchased = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    # Dynamic fields for Recurring Expense
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    frequency = forms.ChoiceField(
        choices=Recurring.FREQUENCY_CHOICES, 
        required=False
    )
    is_loan = forms.BooleanField(
        required=False, 
        initial=False
    )
    
    # Dynamic fields for Loan
    principal = forms.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        required=False
    )
    apr = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False
    )
    term_amt = forms.IntegerField(
        required=False
    ) 
    

class CategoryForm(Form):
    name = forms.CharField(
        max_length=50
    )
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        category_set = Category.objects.values_list("name", flat=True)
        
        if name in category_set:
            raise forms.ValidationError("Category already exists. Please choose a different name.")
        
        return name