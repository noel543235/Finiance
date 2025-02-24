from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Expense(models.Model):

    class Meta:
        db_table = 'user_expenses'
        ordering = ['amount']

    FREQUENCY_CHOICES = [
        ('One-Time', 'One-Time'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='One-Time')
    
    def __str__(self):
        return f"{self.label}: ${self.amount} ({self.get_frequency_display()})"
    
class Loan(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    principal = models.FloatField()
    interest_rate = models.FloatField()
    term = models.IntegerField()
    start_date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.id) + ' - ' + self.label + self.start_date