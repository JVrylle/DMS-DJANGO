from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Patient


def website(request):
    return render(request, 'website.html')

def user_dash(request):
    return render(request, 'User/user_dash.html')

def dentist_dash(request):
    return render(request, 'Dentist/dentist_dash.html')

def admin_dash(request):
    return render(request, 'Admin/admin_dash.html')

def testing(request):
    testing_list = [1,2,3,4,5]

    context = {
        'testing_list': testing_list
    }

    return render(request, 'testing.html', context)