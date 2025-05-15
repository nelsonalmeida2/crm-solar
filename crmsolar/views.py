from django.shortcuts import render
from .models import Company

def index_view(request):
    companies = Company.objects.all()
    return render(request, 'crmsolar/index.html', {'companies': companies})
# Create your views here.
