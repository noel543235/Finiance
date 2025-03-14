from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from accountinfo.models import CustomUser

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Invalid login
            messages.success(request, "There was an error logging in. Please try again")
            return redirect('login')
    else:
        return render(request, 'authentication/login.html', {})
    
def signup_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1!=password2:
            messages.success(request, "Passwords do not match. Please try again")
            return redirect('signup')
        
        if CustomUser.objects.filter(username=username):
            messages.success(request, "Username already in use. Please try again")
            return redirect('signup')
        
        if CustomUser.objects.filter(email=email):
            messages.success(request, "Email already in use. Please try again")
            return redirect('signup')

        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.save()
        login(request, user)
        messages.success(request, "User added successfully")
        return redirect("home")
    else:
        return render(request, 'authentication/signup.html', {})

    