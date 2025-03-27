from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from itertools import chain
from .forms import ExpenseForm, OneTimeForm, SubscriptionForm, LoanForm
from .models import OneTime, Subscription, Loan, Expense
import io
import polars as pl

def add_expense(request):
    """Handles adding a new expense for the logged-in user."""

    if not request.user.is_authenticated:
        return redirect('/login/login')

    expense_form = None
    selected_expense_type = None

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense_type = form.cleaned_data["expense_type"]
            selected_expense_type = expense_type

            # Determine the correct form to use based on selected expense type
            if expense_type == 'O':
                expense_form = OneTimeForm(request.POST)
            elif expense_type == 'S':
                expense_form = SubscriptionForm(request.POST)
            elif expense_type == 'L':
                expense_form = LoanForm(request.POST)
            
            if expense_form and expense_form.is_valid():
                expense = expense_form.save(commit=False)
                expense.user = request.user  # Associate expense with the logged-in user
                expense.save()
                return redirect("expenses")

    else:  # Handle GET request
        form = ExpenseForm()
        selected_expense_type = request.GET.get('expense_type', None)

    return render(request, "expenses/add_expense.html", {
        "form": form,
        "expense_form": expense_form,
        "selected_expense_type": selected_expense_type
    })

def load_expense_form(request):
    """Loads the specific form based on the selected expense type."""
    expense_type = request.GET.get('expense_type')

    # Handle form creation based on expense_type
    if expense_type == 'O':
        form = OneTimeForm()
    elif expense_type == 'S':
        form = SubscriptionForm()
    elif expense_type == 'L':
        form = LoanForm()
    else:
        form = None

    # If form is valid, return the form HTML rendered as a string
    if form:
        form_html = form.as_p()
        return JsonResponse({"form_html": form_html})
    else:
        return JsonResponse({"form_html": ""}, status=400)


def expense_list(request):
    """Displays a list of expenses for the logged-in user, sorted by date."""

    if not request.user.is_authenticated:
        return redirect('/login/login')

    expenses = chain(
        OneTime.objects.filter(user=request.user),
        Subscription.objects.filter(user=request.user),
        Loan.objects.filter(user=request.user)
    )
    
    return render(request, "expenses/expenses.html", {"expenses": expenses})

def delete_expense(request, expense_id):
    """Deletes an expense if it belongs to the logged-in user."""

    if not request.user.is_authenticated:
        return redirect('/login/login')

    if request.method == "POST":

        # Retrieve the expense, ensuring it belongs to the current user
        expense = get_object_or_404(Expense, id=expense_id, user=request.user) 
        expense.delete()
    return redirect('expenses')

def import_expenses(request):
    return render(request, 'expenses/import_expenses.html')
    
def clean_data(df: pl.DataFrame) -> dict:

    # Columns that might already be present
    expected_cols = {"label", "amount", "category", "startDate", "frequency", "principal", "interestRate", "termLength"}    

    # Step 1: Find matching columns
    matching = [col_df for col_df in df.columns if col_df.lower() in expected_cols]

    # Check for other possible column names
    for col in ["name", "description", "date"]:
        
        # Convert column names to lowercase and compare
        matching_columns = [col_df for col_df in df.columns if col_df.lower() == col]
        
        # Rename any found matches to match our expected data format
        if matching_columns:
            if col == "name":
                matching.append("label")
                df = df.rename({"name": "label"})
            elif col == "description":
                matching.append("label")
                df = df.rename({"description": "label"})
            elif col == "date":
                matching.append("startDate")
                df = df.rename({"date": "startDate"})


    # Create a new DataFrame with matching columns
    df_clean = df.select(matching)

    # Add missing columns (if any) with null values
    for col in expected_cols:
        if col not in df_clean.columns:
            df_clean = df_clean.with_columns(pl.lit(None).alias(col))

    # Reorder the columns to match the expected order
    df_clean = df_clean.select(sorted(list(expected_cols)))

    # Check if some data was extracted
    if df_clean.drop_nulls().is_empty():
        error = "All values in the dataset are null. Please upload a valid file."
        raise ValueError(error)

    # Step 2: Find Recurring expenses
    return df_clean.to_dict()

def import_data(request):
    if request.method == "POST" and request.FILES["file"]:
        uploaded_file = request.FILES["file"]

        # Handle CSV file with Polars
        if uploaded_file.name.endswith('.csv'):
            try:
                # Convert the uploaded file to a file-like object using io.BytesIO
                file_like_object = io.BytesIO(uploaded_file.read())

                # Read the CSV file using Polars
                df = pl.read_csv(file_like_object,truncate_ragged_lines=True)

                if request.POST.get('cleaned') == 'on':
                    expected_cols = ["label", "amount", "category", "startDate", "frequency", "principal", "interestRate", "termLength"]

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
                    expected_cols = ["label", "amount", "category", "startDate", "frequency", "principal", "interestRate", "termLength"]

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