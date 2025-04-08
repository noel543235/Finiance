from django.db import models
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now

# User defined categories to group expenses into
class Category(models.Model):

    class Meta:
        db_table = 'categories_table'

    name = models.CharField(max_length=50, unique=True, primary_key=True)

    def __str__(self):
        return f'{self.name}'


# BASE ABSTRACT Expense model from which One Time Expenses and Recurring Expenses inherit from.
# All Expense objects share these fields
class Expense(models.Model):

    class Meta:
        abstract = True

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    label = models.CharField(max_length=50, default="Untitled Expense")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    description = models.TextField(blank=True, null=True, default = "")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, default = None)
    date_created = models.DateTimeField(default=now) # NOTE: This is not when purchase was made, but rather when entry is added to DB


    def __str__(self):
        return f'{self.label} - ${self.amount}'


# One Time Expense Model
class OneTime(Expense):

    class Meta:
        db_table = 'one_time_table'

    date_purchased = models.DateField(default = now)

    def __str__(self):
        return f'{self.label} - ${self.amount}'


# Recurring Expense Model
class Recurring(Expense):

    class Meta:
        abstract = False
        db_table = 'recurring_table'

    # Choices for how often an expense recurs
    FREQUENCY_CHOICES = [
            ('D', 'Daily'),
            ('W', 'Weekly'),
            ('BW', 'Biweekly'),
            ('M', 'Monthly'),
            ('SA', 'Semiannually'),
            ('A', 'Annually'),
            ('BA', 'Biannually')
        ]  

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    frequency = models.CharField(max_length=2, choices=FREQUENCY_CHOICES)    
    
    def when_next_payment(self, start_date):
        '''Calculate the due date of the following payment in schedule'''
        if self.frequency == 'D':
            return start_date + relativedelta(days=1)
        elif self.frequency == 'W':
            return start_date + relativedelta(weeks=1)
        elif self.frequency == 'BW':
            return start_date + relativedelta(weeks=2)
        elif self.frequency == 'M':
            return start_date + relativedelta(months=1)
        elif self.frequency == 'SA':
            return start_date + relativedelta(months=6)
        elif self.frequency == 'A':
            return start_date + relativedelta(years=1)
        else:
            return start_date + relativedelta(years=2)
        
        
    def update_next_payment_date(self, new_date):
        '''Update the due date of the following payment in schedule'''
        self.start_date = new_date
        self.save()

    def __str__(self):
        return f'{self.label} - ${self.amount} - {self.frequency}'


# Loan Model - Inherits from Recurring Expense Model
class Loan(Recurring):

    class Meta:
        db_table = 'loan_table'
        
    principal = models.DecimalField(max_digits=20, decimal_places=2, default=0.00) 
    apr = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)  # Annual Interest Rate
    term_amt = models.IntegerField(default=12) # Months

    # NOTE: Monthly compounding is assumed

    def __str__(self):
        return f'{self.label} - ${self.principal} - {self.apr}'
    
# Loan Payment Model - Represents payments towards loan objects
class LoanPayment(models.Model):

    class Meta:
        db_table = 'loan_payment_table'

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Payment of ${self.amount} on {self.payment_date} toward {self.loan.name}'