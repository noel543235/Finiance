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
    
    def test_input(self):
        form = {
            "present_value": 1000,
            "compounds": 10,
            "interest_rate": 6,
            "periodic_deposit": 100
        }
        
        FV_end = [["1", "$1000.00",	"$100.00",	"$60.00",	"$1160.00"],
                  ["2", "$1160.00",	"$100.00",	"$69.60",	"$1329.60"],
                  ["3", "$1329.60",	"$100.00",	"$79.78",	"$1509.38"],
                  ["4", "$1509.38", "$100.00",	"$90.56",	"$1699.94"],
                  ["5", "$1699.94", "$100.00",  "$102.00",	"$1901.93"],
                  ["6", "$1901.93",	"$100.00",	"$114.12",	"$2116.05"],
                  ["7", "$2116.05",	"$100.00",	"$126.96",	"$2343.01"],
                  ["8", "$2343.01",	"$100.00",	"$140.58",	"$2583.59"],
                  ["9", "$2583.59",	"$100.00",	"$155.02",	"$2838.61"],
                  ["10","$2838.61",	"$100.00",	"$170.32",	"$3108.93"]]
        
        FV_beginning = [["1", "$1100.00", "$100.00", "$66.00", "$1166.00"],
                        ["2", "$1266.00", "$100.00", "$75.96", "$1341.96"],
                        ["3", "$1441.96", "$100.00", "$86.52", "$1528.48"],
                        ["4", "$1628.48", "$100.00", "$97.71", "$1726.19"],
                        ["5", "$1826.19", "$100.00", "$109.57", "$1935.76"],
                        ["6", "$2035.76", "$100.00", "$122.15", "$2157.90"],
                        ["7", "$2257.90", "$100.00", "$135.47",	"$2393.38"],
                        ["8", "$2493.38", "$100.00", "$149.60",	"$2642.98"],
                        ["9", "$2742.98", "$100.00", "$164.58",	"$2907.56"],
                        ["10","$3007.56", "$100.00", "$180.45",	"$3188.01"]]
        
        table1 = future_value_calculator(form["present_value"], form["compounds"], form["interest_rate"], form["periodic_deposit"], "end")
        table2 = future_value_calculator(form["present_value"], form["compounds"], form["interest_rate"], form["periodic_deposit"], "beginning")

        
        for i in range(len(table1)):
            for j in range(len(table1[i])):
                self.assertEqual(table1[i][j], FV_end[i][j])
                self.assertEqual(table2[i][j], FV_beginning[i][j])
    
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
        # url = reverse("savings:calculate")
        
        form = {
            "present_value" : "1000",
            "compounds" : "10",
            "interest_rate": "6",
            "periodic_deposit": "100"
        }
        
        # response = self.client.post(url, form)
        
        # self.assertIn("table", response.context)
        # self.assertIsInstance(response.context["table"], list)
     
        
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
        

