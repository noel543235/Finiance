from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from expenses.models import Category, Recurring
# SAVINGS ABSTRACT MODEL ---------------------------------------------------------

class Saving(models.Model):

    class Meta:
        abstract = True

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=50, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    
    
class SavingsAccount(Saving):
    
    class Meta:
        db_table = 'savings_account_table'
    
    COMPOUND_CHOICES = [
        ('M', 'Months'),
        ('Y', 'Years')
    ]
    
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    compound = models.CharField(
        max_length = 1,
        choices = COMPOUND_CHOICES,
        default = 'M'
    )
    
class SavingsGoal(Saving):
    
    class Meta:
        db_table = 'savings_goal_table'
        
    contribution = models.DecimalField(decimal_places=2, max_digits=10, default=0.0) 
    frequency = models.CharField(
        max_length = 2,
        choices = Recurring.FREQUENCY_CHOICES,
        default = 'M'
    )
        
        
        
        