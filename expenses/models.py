from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

FREQUENCY_CHOICES = [
        ('O', 'One Time'),
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('A', 'Annually'),
        ('BW', 'Biweekly')
    ]

class Category(models.Model):
    
    class Meta:
        db_table = 'categories_table'
    
    name = models.CharField(max_length=50, unique=True, primary_key=True)
   
# EXPENSE ABSTRACT MODEL ---------------------------------------------------------

class Expense(models.Model):

    class Meta:
        abstract = True

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    
class Loan(Expense):
    
    class Meta:
        db_table = 'loans_table'
    
    TERM_CHOICES = [
        ('M', 'Months'),
        ('Y', 'Years')
    ]
    
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2)
    term_amt = models.IntegerField()
    term = models.CharField(
        max_length = 1,
        choices = TERM_CHOICES,
        default = 'M'
    )
    
    
class Subscription(Expense):
    
    class Meta:
        db_table = 'subscriptions_table'
    
    frequency = models.CharField(
        max_length = 2,
        choices = FREQUENCY_CHOICES,
        default = 'O'
    )
    
    
class OneTime(Expense):
    
    class Meta:
        db_table = 'one_times_table'
        
    pass