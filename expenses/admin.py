from django.contrib import admin
from .models import Expense, Loan

# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    model = Expense
    fieldsets = (
        (None, {'fields': ('user', 'label', 'amount', 'date', 'frequency')}),
    )
    
class LoanAdmin(admin.ModelAdmin):
    model = Loan
    fieldsets = (
        (None, {'fields': ('user', 'label', 'principal', 'interest_rate', 'term', 'start_date')}),
    )

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Loan, LoanAdmin)