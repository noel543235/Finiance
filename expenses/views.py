# Standard Library Imports
import io
import json
from datetime import datetime, timedelta

# Third-Party Imports
import polars as pl

# Django Imports
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

# Local Imports
from .forms import *
from .models import *

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
    
    return render(request, "expenses/expenses.html", context)


def index_context(request):
    # Query all user expenses from database
    recent_expenses = get_recent_expenses(request)
    categories = Category.objects.all()
    
    recurring = Recurring.objects.filter(user=request.user)
    final = [rec for rec in recurring if rec.label not in Loan.objects.values_list('label', flat=True)]
    
    # Create context object to send to template
    context = {
        "recent_expenses": recent_expenses,
        "category_form": CategoryForm,
        "categories": categories,
        "onetimes": OneTime.objects.filter(user=request.user),
        "recurring": final,
        "loans": Loan.objects.filter(user=request.user),
        "today": datetime.today().date(),
        "week_ago": datetime.today().date()-timedelta(weeks=1),
        "total": sum([e.amount for e in recent_expenses])
    }
    
    return context
    

def add_expense(request):
    """Page where user creates expenses

    Args:
        request (HttpRequest): User info

    Returns:
        HttpResponse: Template to load with form
    """
    
    # Create context object containing expense form
    context = add_expense_context(request)
    
    return render(request, "expenses/add_expense.html", context)


def add_expense_context(request):
    # Create context object to send to template
    context = {
        "form": ExpenseForm
    }
    
    return context


def create_expense(request):
    """View to process form and create expenses

    Args:
        request (HttpRequest): Form info

    Returns:
        HttpRedirect: Redirect to index page
    """
    form = ExpenseForm(request.POST)
    if form.is_valid():
        is_recurring = form.cleaned_data['is_recurring']
        is_loan = form.cleaned_data['is_loan']

        if not is_recurring:
            # Handle one-time expense
            one_time_expense = OneTime(
                user=request.user,
                label=form.cleaned_data['label'],
                amount=form.cleaned_data['amount'],
                description=form.cleaned_data['description'],
                category=form.cleaned_data['category'],
                date_created=datetime.now(),
                start_date=form.cleaned_data['date_purchased']
            )
            one_time_expense.save()
        else:
            if not is_loan:
                # Handle recurring expense
                recurring_expense = Recurring(
                    user=request.user,
                    label=form.cleaned_data['label'],
                    amount=form.cleaned_data['amount'],
                    description=form.cleaned_data['description'],
                    category=form.cleaned_data['category'],
                    date_created=datetime.now(),
                    start_date=form.cleaned_data['start_date'],
                    end_date=form.cleaned_data['end_date'],
                    frequency=form.cleaned_data['frequency'],
                )
                recurring_expense.save()
            
            else:
                # Handle loan expense
                loan_expense = Loan(
                    user=request.user,
                    label=form.cleaned_data['label'],
                    amount=form.cleaned_data['amount'],
                    description=form.cleaned_data['description'],
                    category=form.cleaned_data['category'],
                    date_created=datetime.now(),
                    start_date=form.cleaned_data['start_date'],
                    end_date=form.cleaned_data['end_date'],
                    frequency=form.cleaned_data['frequency'],
                    principal=form.cleaned_data['principal'],
                    apr=form.cleaned_data['apr'],
                    term_amt=form.cleaned_data['term_amt']
                )
                loan_expense.save()
                
    else:
        # Form is invalid, return the form with errors
        context = add_expense_context(request)
        context["form"] = form
        return render(request, 'expenses/add_expenses.html', context)
                

    return redirect("expenses:index")


def create_category(request):
    """View to process form and create categories

    Args:
        request (HttpRequest): Form info

    Returns:
        HttpRedirect: Redirect to index page
    """
    form = CategoryForm(request.POST)
    if form.is_valid():
        # Helper variable for cleaned form data
        f = form.cleaned_data
        
        category = Category(
            name=f['name']
        )
        category.save()
        
    else:
        # Form is invalid, return the form with errors
        context = index_context(request)
        context["category_form"] = form
        return render(request, 'expenses/expenses.html', context)
    
    return redirect("expenses:index")
        

def delete_expense(request, expense_id):
    """Deletes an expense

    Args:
        request (HttpRequest): User info
        expense_id (int): PK identifying expense

    Returns:
        HttpRedirect: Redirect to index page
    """
    
    if not request.user.is_authenticated:
        return redirect('/login/login')
    
    # Initialize expense
    expense = None
    
    # Check if expense is OneTime
    try:
        expense = OneTime.objects.get(id=expense_id)
    except OneTime.DoesNotExist:
        pass
    
    # Check if expense is Recurring
    try:
        expense = Recurring.objects.get(id=expense_id)
    except Recurring.DoesNotExist:
        pass

    if request.method == "POST":

        # Retrieve the expense, ensuring it belongs to the current user
        expense.delete()
            
            
    return redirect('expenses:index')


def get_recent_expenses(request):
    today = datetime.today().date()
    week_ago = today-timedelta(weeks=1)

    onetime_expenses = OneTime.objects.filter(user=request.user, start_date__gte=week_ago)
    recurring_expenses = list()
    
    for expense in Recurring.objects.filter(user=request.user):
        payment_date = expense.start_date
        while payment_date <= today and ((expense.end_date is None) or expense.end_date >= today):
            if payment_date >= week_ago:
                recurring_expenses.append(copy_expense(expense, payment_date))
            payment_date = expense.when_next_payment(payment_date)  
                
    return sorted(recurring_expenses + list(onetime_expenses), key=lambda x: x.start_date, reverse=True)


def copy_expense(orig, day):
    new = Recurring()
    for field in orig._meta.fields:
        setattr(new, field.name, getattr(orig, field.name))
        
    new.start_date = day
        
    return new


def import_expenses(request):
    return render(request, 'expenses/import_expenses.html')


def clean_data(df: pl.DataFrame) -> dict:

    # Columns that might already be present
    expected_cols = {"label", "amount", "category", "startdate",
                     "frequency", "principal", "interestRate", "termLength"}

    # Step 1: Find matching columns

    # Map lowercase names to actual column names
    col_map = {col.lower(): col for col in df.columns}

    # Define potential names and map them to the correct casing
    name_aliases = ["name", "description"]
    date_aliases = ["date"]

    # Handle name/description mapping
    for alias in name_aliases:
        if alias in col_map:
            df = df.rename({col_map[alias]: "Label"})

    # Handle date mapping
    for alias in date_aliases:
        if alias in col_map:
            df = df.rename({col_map[alias]: "startDate"})

    # See which columns match the expected name
    matching = [col_df for col_df in df.columns if col_df.lower()
                in expected_cols]

    # Create a new DataFrame with matching columns
    df_clean = df.select(matching)

    # Add missing columns (if any) with null values
    for col in expected_cols:
        if col not in {col_df.lower() for col_df in df_clean.columns}:
            df_clean = df_clean.with_columns(pl.lit(None).alias(col))

    # Check if some data was extracted
    if (sum(df_clean.null_count().sum()) == df_clean.shape[0] * df_clean.shape[1])[0]:
        error = "Data could not be extracted. Please upload a valid file."
        raise ValueError(error)

    # Step 2: Find Recurring expenses

    try:
        # Ensure "startDate" is in date format
        df_clean = df_clean.with_columns(
            pl.col("startDate").cast(pl.Date).alias("startDate"))
    except Exception as e:
        raise ValueError("Error casting date, please ensure date is in YYYY-MM-DD") from e

    if df_clean['frequency'].is_null().all():
        # Group by label and amount and check for duplicates
        df_grouped = df_clean.group_by(["Label", "Amount"]).agg([

            # Store the smallest startDate as min_startDate
            pl.col("startDate").min().alias("min_startDate"),

            # Calculate the smallest difference in start dates
            pl.col("startDate").sort().diff().min().alias("date_diff"),

            # Counts how many times any one label appears
            pl.col("startDate").count().alias("count"),
        ])

        # Iterate through the groups and determine the frequency
        df_final = df_clean.join(df_grouped, on=["Label", "Amount"], how="left")

        def set_frequency(row):
            """Assigns frequency based on date difference and occurrence count."""

            count = row['count']
            date_diff = row['date_diff']

            if count == 1:
                return None  # One-time expense
            elif date_diff.days >= 5 and date_diff.days <= 9:
                return "Weekly"
            elif date_diff.days >= 12 and date_diff.days <= 16:
                return "Biweekly"
            elif date_diff.days >= 28 and date_diff.days <= 32:
                return "Monthly"
            elif date_diff.days >= 178 and date_diff.days <= 182:
                return "Semiannually"
            elif date_diff.days >= 363 and date_diff.days <= 367:
                return "Annually"
            elif date_diff.days >= 728 and date_diff.days <= 732:
                return "Biannually"
            else:
                return None  # Irregular or unknown frequency

        # Set frequency based on the date difference and count
        df_final = df_final.with_columns(
            pl.struct(["count", "date_diff"])
            .map_elements(lambda row: set_frequency(row), return_dtype=pl.Utf8)
            .alias("frequency")
        )

        # Remove duplicate rows based on the label, keeping the first entry
        df_final = df_final.sort("startDate").unique(
            subset=["Label","Amount"], keep="first")

        # Select all columns except the three that were used for frequency
        df_final = df_final.select(df_final.columns[:-3])

        # Convert the date into a string that can be parsed by Python
        df_final = df_final.with_columns(pl.col("startDate").cast(pl.String))

        # Order the columns
        df_final = df_final.select(["Label", "Amount", "Category", "startDate", "frequency", "principal", "interestRate", "termLength"])

        # Sort by start date
        df_final = df_final.sort("startDate")

        return df_final.to_dicts()
    else:

        # Order the columns
        df_clean = df_clean.select(["Label", "Amount", "Category", "startDate", "frequency", "principal", "interestRate", "termLength"])

        df_clean = df_clean.sort("startDate")

        return df_clean.to_dicts()


def import_data(request):
    if request.method == "POST" and request.FILES["file"]:
        uploaded_file = request.FILES["file"]

        # Handle CSV file with Polars
        if uploaded_file.name.endswith('.csv'):
            try:
                # Convert the uploaded file to a file-like object using io.BytesIO
                file_like_object = io.BytesIO(uploaded_file.read())

                # Read the CSV file using Polars
                df = pl.read_csv(file_like_object, truncate_ragged_lines=True)

                if request.POST.get('cleaned') == 'on':
                    expected_cols = ["label", "amount", "category", "startDate",
                                     "frequency", "principal", "interestRate", "termLength"]

                    # Check for missing or extra columns
                    missing_cols = [col for col in expected_cols if col not in df.columns]
                    extra_cols = [col for col in df.columns if col not in expected_cols]

                    if missing_cols or extra_cols:
                        error = "Column names do not match."
                        if missing_cols:
                            error += f" Missing columns: {missing_cols}."
                        if extra_cols:
                            error += f" Extra columns: {extra_cols}."
                        return render(request, 'expenses/import_expenses.html', {'error': error})

                    # Convert the DataFrame to a list of dictionaries for easy rendering in templates
                    data = df.to_dicts()

                else:
                    data = clean_data(df)
                
                # Pass the data to the template
                return render(request, 'expenses/upload_result.html', {'data': data})

            except Exception as e:
                return render(request, 'expenses/import_expenses.html', {'error': f"Error reading CSV file: {str(e)}"})

        # Handle JSON file with Polars
        elif uploaded_file.name.endswith('.json'):
            try:
                # Convert the uploaded file to a file-like object using io.BytesIO
                file_like_object = io.BytesIO(uploaded_file.read())

                # Read the JSON file using Polars
                df = pl.read_json(file_like_object)

                if request.POST.get('cleaned') == 'on':
                    expected_cols = ["label", "amount", "category", "startDate",
                                     "frequency", "principal", "interestRate", "termLength"]

                    # Check for missing or extra columns
                    missing_cols = [col for col in expected_cols if col not in df.columns]
                    extra_cols = [col for col in df.columns if col not in expected_cols]

                    if missing_cols or extra_cols:
                        error = "Column names do not match."
                        if missing_cols:
                            error += f" Missing columns: {missing_cols}."
                        if extra_cols:
                            error += f" Extra columns: {extra_cols}."
                        return render(request, 'expenses/import_expenses.html', {'error': error})

                    # Convert the DataFrame to a list of dictionaries for easy rendering in templates
                    data = df.to_dicts()

                else:
                    data = clean_data(df)

                # Pass the data to the template
                return render(request, 'expenses/upload_result.html', {'data': data})

            except Exception as e:
                return render(request, 'expenses/import_expenses.html', {'error': f"Error reading JSON file: {str(e)}"})

        else:
            return render(request, 'expenses/import_expenses.html', {'error': "Invalid file type. Please upload a CSV or JSON file."})

    return render(request, 'expenses/import_expenses.html')


def import_result(request):
    if request.method == "POST":
        data = json.loads(request.body).get("data", [])
        for row in data:
            # Check and create category if it doesn't exist
            category_name = row.get("CSategory")
            category = None
            if category_name:
                # Get or create the category
                category, created = Category.objects.get_or_create(name=category_name)
            try:
                if row['StartDate']:
                    date = timezone.make_aware(datetime.strptime(row['StartDate'], "%Y-%m-%d"), timezone.get_current_timezone())
                else:
                    date = timezone.now()
            except ValueError:
                return JsonResponse({"error": "Error: Date could not be converted. Please use 'YYYY-MM-DD' (e.g., 2024-03-31)."}, status=400)

            frequency = {"None": "O", "Daily": "D", "Weekly": "W", "Biweekly": "BW", "Monthly": "M",
                         "Semiannually": "SA", "Annually": "A", "Biannually": "BA"}[row['Frequency'].strip()]

            if frequency == "O":
                OneTime.objects.create(
                    user = request.user,
                    label = row['Label'],
                    amount = row['Amount'],
                    start_date = date,
                    description = "",
                    category = category
                    )
            elif row['Principal'] == "None" or row['TermLength'] == "None" or row['InterestRate'] == "None":
                Recurring.objects.create(
                    user = request.user,
                    label = row['Label'],
                    amount = row['Amount'],
                    start_date = date,
                    description = "",
                    category = category,
                    frequency = frequency
                )
            else:
                Loan.objects.create(
                    user = request.user,
                    label = row['Label'],
                    amount = row['Amount'],
                    start_date = date,
                    description = "",
                    category = category,
                    frequency = frequency,
                    apr = row['InterestRate'],
                    term_amt = row['TermLength'],
                    principal = row['Principal']
                )
        return JsonResponse({"message": "Data received successfully!"})
    