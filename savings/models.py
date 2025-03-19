from django.db import models
from expenses.models import Recurring
  
# Savings Goal Class
class SavingsGoal(Recurring):
    
    class Meta:
        db_table = 'savings_goal_table'
    

# Savings Goal Payment Class
class GoalPayment(models.Model):
    
    class Meta:
        db_table = 'goal_payment_table'
        
    goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
            return f'Payment of ${self.amount} on {self.payment_date} toward {self.goal.name}'
    
        
        
        
        