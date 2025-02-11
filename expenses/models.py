from django.db import models
from accountinfo.models import CustomUser

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

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='One-Time')
    
    def __str__(self):
        return f"{self.label}: ${self.amount} ({self.get_frequency_display()})"