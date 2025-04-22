from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import SavingsGoal
from datetime import datetime

@receiver(post_save, sender=User)
def create_default_savings_goals(sender, instance, created, **kwargs):
    if created:
        SavingsGoal.objects.create(
            user=instance,
            label='Retirement',
            amount=50000,
            frequency='M',
            payment_amount=250.00,
            start_date=datetime.now(),
            category=None,
            date_created=datetime.now(),
        )
        SavingsGoal.objects.create(
            user=instance,
            label='Emergency Fund',
            amount=5000,
            frequency='M',
            payment_amount=150.00,
            start_date=datetime.now(),
            category=None,
            date_created=datetime.now(),
        )