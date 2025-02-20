from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Savings(models.Model):
    
    FREQUENCY_CHOICES = [
        ('One-Time', 'One-Time'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
    ]
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='One-Time')
    start_date = models.DateField(default=timezone.now)
    

    def __str__(self):
        return str(self.id) + ' - ' + self.label + self.start_date