from django.contrib import admin
from .models import *

# Register your models here.
   
class SavingsGoalAdmin(admin.ModelAdmin):
    model = SavingsGoal
    fieldsets = (
        (None, {'fields': ('label', 'amount', 'start_date', 'frequency', 'next_due_date', 'end_date', 'category')}),
    )
   
    
class GoalPaymentAdmin(admin.ModelAdmin):
    model = GoalPayment
    fieldsets = (
        (None, {'fields': ('goal', 'payment_date', 'amount')}),
    )
    

admin.site.register(SavingsGoal, SavingsGoalAdmin)
admin.site.register(GoalPayment, GoalPaymentAdmin)