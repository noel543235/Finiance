# Standard Library Imports
import io
import json
from datetime import datetime
from itertools import chain

# Third-Party Imports
import polars as pl

# Django Imports
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.forms.models import model_to_dict

# Local Imports
from .models import *
from datetime import datetime, timedelta
from expenses.models import *
from savings.models import *
from savings.views import getGoalPercentages, get_payments


def index(request):
    """Initial template when user visits expenses page

    Args:
        request (HttpRequest): User info

    Returns:
        HttpResponse: Template to load with context (forms, expenses, etc.)
    """
    
    # Redirects user to login page if they are not logged in
    if not request.user.is_authenticated:
        return redirect('/login/login')
    
    # Create context object to send to template
    context = index_context(request)
    
    return render(request, "accountinfo/index.html", context)


def index_context(request):  
    goals = SavingsGoal.objects.filter(user=request.user)
    # Create context object to send to template
    context = {
        "recurring_expenses": Recurring.objects.filter(user=request.user),
        "savings_goals": goals,
        "payments": get_payments(request, goals),
        "user": request.user,
    }
    
    return context