from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import (
    District,
    Country,
    Address,
    Segment,
    BuildingType,
    Observation,
    Contact,
    Company,
    CompanyGroup,
    Provider,
    CPE,
    OpportunityStatus,
    Product,
    Opportunity,
    CalendarEntry,
    TaskType,
    Task,
)


@login_required
def index_view(request):
    companies = Company.objects.all()
    return render(request, 'crmsolar/index.html', {'companies': companies})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redireciona para a página inicial depois de login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'crmsolar/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
