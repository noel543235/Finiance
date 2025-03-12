from django.shortcuts import render

def index(request): 
    return render(request, "home/homepage.html", {})

def history(request): 
    return render(request, "home/history.html", {})