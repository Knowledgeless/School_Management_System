from django.shortcuts import render, redirect
from django.contrib.auth import login
from . import forms
# Create your views here.


def home(request):
    return render(request, "html/home.html")

def add_person(request):
    if request.method == "POST":
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            # Store role in session or future user profile model
            user.profile.role = form.cleaned_data['role']  
            user.profile.save()
            login(request, user)  # Auto-login after registration
            return redirect("home")  # Redirect to homepage
    else:
        form = forms.CustomUserCreationForm()
    return render(request, "html/add_person.html", {"form":form})

def teachers_list(request):
    return render(request, "html/teachers_list.html")

def students_list(request):
    return render(request, "html/students_list.html")

def grade(request):
    return render(request, "html/grade.html")

def attendence(request):
    return render(request, "html/attendence.html")

def admit_card(request):
    return render(request, "html/admit_card.html")

def tickets(request):
    return render(request, "html/tickets.html")