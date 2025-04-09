from django.contrib import admin
from .models import *

# Register your models here.
   
class SavingsGoalAdmin(admin.ModelAdmin):
    model = SavingsGoal
    fieldsets = (
        (None, {'fields': ('user', 'label', 'goal_amount', 'amount', 'start_date', 'frequency', 'category')}),
    )
   
    
class GoalPaymentAdmin(admin.ModelAdmin):
    model = GoalPayment
    fieldsets = (
        (None, {'fields': ('goal', 'payment_date', 'amount')}),
    )
    

admin.site.register(SavingsGoal, SavingsGoalAdmin)
admin.site.register(GoalPayment, GoalPaymentAdmin)