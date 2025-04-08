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
from .forms import *
from .models import *


def add_expense(request):
    """Handles adding a new expense for the logged-in user."""

    # Redirects user to login page if they are not logged in
    if not request.user.is_authenticated:
        return redirect('/login/login')

    # Initialize general form allowing user to select one-time or recurring expense
    form = ExpenseForm()

    if request.method == 'POST':
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
                    date_purchased=form.cleaned_data['date_purchased']
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

    return render(request, "expenses/add_expense.html", {'form': form})


def expense_list(request):
    """Displays a list of expenses for the logged-in user, sorted by date."""

    if not request.user.is_authenticated:
        return redirect('/login/login')

    onetime_expenses = OneTime.objects.filter(user=request.user)
    recurring_expenses = Recurring.objects.filter(user=request.user)

    return render(request, "expenses/expenses.html", {"onetime_expenses": onetime_expenses, "recurring_expenses": recurring_expenses})

def delete_onetime_expense(request, expense_id):
    """Deletes an expense if it belongs to the logged-in user."""

    if not request.user.is_authenticated:
        return redirect('/login/login')

    expense = get_object_or_404(OneTime, pk=expense_id)

    if request.method == "POST":

        # Retrieve the expense, ensuring it belongs to the current user
        expense.delete()

        # expense.delete()


    return redirect('expenses')


def delete_recurring_expense(request, expense_id):
    """Deletes an expense if it belongs to the logged-in user."""
    
    if not request.user.is_authenticated:
        return redirect('/login/login')

    expense = get_object_or_404(Recurring, pk=expense_id)

    if request.method == "POST":
            
        # Retrieve the expense, ensuring it belongs to the current user
        expense.delete()

        # expense.delete()


    return redirect('expenses')


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
        # Raise a custom error message if casting fails
        raise ValueError("Error casting date, please ensure date is in YYYY-MM-DD") from e

    if df_clean['frequency'].is_null().all():
        # Group by label and check for duplicates
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
            category_name = row.get("category")
            category = None
            if category_name:
                # Get or create the category
                category, created = Category.objects.get_or_create(name=category_name)
            try:
                if row['startDate']:
                    date = timezone.make_aware(datetime.strptime(row['startDate'], "%Y-%m-%d"), timezone.get_current_timezone())
                else:
                    date = timezone.now()
            except ValueError:
                return JsonResponse({"error": "Error: Date could not be converted. Please use 'YYYY-MM-DD' (e.g., 2024-03-31)."}, status=400)

            frequency = {"None": "O", "Daily": "D", "Weekly": "W", "Biweekly": "BW", "Monthly": "M",
                         "Semiannually": "SA", "Annually": "A", "Biannually": "BA"}[row['frequency'].strip()]

            if frequency == "O":
                OneTime.objects.create(
                    user = request.user,
                    label = row['label'],
                    amount = row['amount'],
                    date_purchased = date,
                    description = "",
                    category = category
                    )
            elif row['principal'] == "None" or row['termLength'] == "None" or row['interestRate'] == "None":
                Recurring.objects.create(
                    user = request.user,
                    label = row['label'],
                    amount = row['amount'],
                    start_date = date,
                    description = "",
                    category = category,
                    frequency = frequency
                )
            else:
                Loan.objects.create(
                    user = request.user,
                    label = row['label'],
                    amount = row['amount'],
                    start_date = date,
                    description = "",
                    category = category,
                    frequency = frequency,
                    apr = row['interestRate'],
                    term_amt = row['termLength'],
                    principal = row['principal']
                )
        return JsonResponse({"message": "Data received successfully!"})
