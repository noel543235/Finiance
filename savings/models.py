from django.db import models
from expenses.models import Expense, Recurring
from dateutil.relativedelta import relativedelta
  
from expenses.models import Expense, Recurring
from dateutil.relativedelta import relativedelta
  
  
# Savings Goal Class
class SavingsGoal(Expense):
class SavingsGoal(Expense):
    
    class Meta:
        db_table = 'savings_goal_table'
        
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=2, choices=Recurring.FREQUENCY_CHOICES)
    start_date = models.DateField()
    
    def when_next_payment(self):
        '''Calculate the due date of the following payment in schedule'''
        if self.frequency == 'D':
            return self.start_date + relativedelta(days=1)
        elif self.frequency == 'W':
            return self.start_date + relativedelta(weeks=1)
        elif self.frequency == 'BW':
            return self.start_date + relativedelta(weeks=2)
        elif self.frequency == 'M':
            return self.start_date + relativedelta(months=1)
        elif self.frequency == 'SA':
            return self.start_date + relativedelta(months=6)
        elif self.frequency == 'A':
            return self.start_date + relativedelta(years=1)
        else:
            return self.start_date + relativedelta(years=2)
        
        
    def update_next_payment_date(self, new_date):
        '''Update the due date of the following payment in schedule'''
        self.start_date = new_date
        self.save()
        
    def __str__(self):
        return f'{self.label} - ${self.amount} - {self.frequency}'
    

# Savings Goal Payment Class
class GoalPayment(models.Model):
    
    class Meta:
        db_table = 'goal_payment_table'
        
    goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
            return f'Payment of ${self.amount} on {self.payment_date} toward {self.goal.label}'
    
        
        
        
        