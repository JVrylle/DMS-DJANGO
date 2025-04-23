from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Patient

# WEBSITE
def website(request):
    return render(request, 'website.html')

# USER
def user_dash(request):
    return render(request, 'User/user_dash.html')

# def user_landing(request):
#     return render(request, 'User/user_landing.html')

def user_appointments(request):
    return render(request, 'User/user_appointments.html')

def user_analytics(request):
    return render(request, 'User/user_analytics.html')

def user_notifications(request):
    return render(request, 'User/user_notifications.html')

def user_prescription(request):
    return render(request, 'User/user_prescription.html')

def user_health_record(request):
    return render(request, 'User/user_health_record.html')

def user_emergency(request):
    return render(request, 'User/user_emergency.html')

def user_faq(request):
    return render(request, 'User/user_faq.html')




# DENTIST
def dentist_dash(request):
    return render(request, 'Dentist/dentist_dash.html')

# ADMIN
def admin_dash(request):
    return render(request, 'Admin/admin_dash.html')




# TESTING
def testing(request):
    testing_list = [1,2,3,4,5]

    context = {
        'testing_list': testing_list
    }

    return render(request, 'testing.html', context)