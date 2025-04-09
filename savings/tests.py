from django.test import TestCase, SimpleTestCase
from .views import future_value_calculator
from django.urls import reverse
from .models import SavingsGoal, GoalPayment
from expenses.models import Category
from django.contrib.auth.models import User
from datetime import date
from dateutil.relativedelta import relativedelta
from .views import getGoalPayments

# Create your tests here.
class FVCTest(TestCase):
    def test_future_value_calculations(self):
        form = {
            "present_value": 1000,
            "compounds": 10,
            "interest_rate": 6,
            "periodic_deposit": 100
        }
        FV = [
            "$1160.00",
            "$1329.60",
            "$1509.38",
            "$1699.94",
            "$1901.93",
            "$2116.05",
            "$2343.01",
            "$2583.59",
            "$2838.61",
            "$3108.93"
        ]
        
        table = future_value_calculator(form["present_value"], form["compounds"], form["interest_rate"], form["periodic_deposit"])
        
        for i in range(len(table)):
            self.assertEqual(table[i][4], FV[i])
    
    def test_calculate_call(self):
        url = reverse("calculate")
        
        form = {
            "present_value" : "1000",
            "compounds" : "10",
            "interest_rate": "6",
            "periodic_deposit": "100"
        }
        
        response = self.client.post(url, form)
        
        self.assertIn("table", response.context)
        self.assertIsInstance(response.context["table"], list)
        
        class SavingsGoalTest(TestCase):
    def setUp(self):
        # Create test user
        self.test_user = User.objects.create_user(
            username='test',
            password='1234'
        )
        
        # Create test category
        self.test_category = Category.objects.create(
            name='Europe'
        )
        
        # Create test savings goal
        self.savings_goal = SavingsGoal.objects.create(
            user=self.test_user,
            label='Europe Vacation',
            amount=2500.00,
            description='Flights & rentals for April 5th 2026 vacation.',
            category=self.test_category,
            payment_amount=250.00,
            frequency='M',
            start_date=date(2025, 6, 21)              
        )
        
    
    def validate_values(self):
        self.assertEqual(self.savings_goal.user, self.test_user)
        self.assertEqual(self.savings_goal.label, 'Europe Vacation')
        self.assertEqual(self.savings_goal.amount, 2500.00)
        self.assertEqual(self.savings_goal.description, 'Flights & rentals for April 5th 2026 vacation.')
        self.assertEqual(self.savings_goal.category, self.test_category)
        self.assertEqual(self.savings_goal.frequency, 'D')
        self.assertEqual(self.savings_goal.start_date, date(2025, 6, 21))
        
    
    def test_calculate_next_payment(self):
        cur_date = self.savings_goal.start_date
        next_date = cur_date + relativedelta(months=1)
        self.assertEqual(self.savings_goal.when_next_payment(), next_date)
        
        

class GoalPaymentTest(TestCase):
    def setUp(self):
        # Create test user
        self.test_user = User.objects.create_user(
            username='test_v2.0',
            password='5678'
        )
        
        # Create test category
        self.test_category = Category.objects.create(
            name='Bob Owes Me'
        )
        
        # Create test savings goal
        self.savings_goal = SavingsGoal.objects.create(
            user=self.test_user,
            label='Epic Universe Tickets',
            amount=575.99,
            description='Epic Universe 2-day tickets and parking',
            category=self.test_category,
            payment_amount=50.00,
            frequency='W',
            start_date=date(2025, 5, 14)              
        )
        
        # Create test goal payment 1
        self.goal_payment1 = GoalPayment.objects.create(
            goal=self.savings_goal,
            amount=75.00,
            payment_date = date.today()
        )
        
        # Create test goal payment 2
        self.goal_payment2 = GoalPayment.objects.create(
            goal=self.savings_goal,
            amount=13.98,
            payment_date = date(2025, 3, 15) 
        )
        
        
    def validate_values(self):
        self.assertEqual(self.goal_payment1.goal, self.savings_goal)
        self.assertEqual(self.goal_payment1.amount, 75.00)
        self.assertEqual(self.goal_payment1.payment_date, date.today())
        
        self.assertEqual(self.goal_payment2.goal, self.savings_goal)
        self.assertEqual(self.goal_payment2.amount, 13.98)
        self.assertEqual(self.goal_payment2.payment_date, date(2025, 3, 15))
        
        
    def test_payment_system(self):
        payments = getGoalPayments(self.savings_goal)
        total = 0
        for payment in payments:
            total += payment.amount
            
        self.assertEqual(float(total), 13.98 + 75.00)
        

