from django.test import TestCase, SimpleTestCase
from .views import future_value_calculator
from django.urls import reverse

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
        
        