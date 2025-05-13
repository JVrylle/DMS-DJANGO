from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required
from .forms import PatientForm, ConsentForm, IntraoralExaminationForm
from .models import Patient, IntraoralExamination


# USER
@role_required(['USER'])
def user_dash(request):
    return render(request, 'User/user_dash.html')

@role_required(['USER'])
def user_appointments(request):
    return render(request, 'User/user_appointments.html')

@role_required(['USER'])
def user_analytics(request):
    return render(request, 'User/user_analytics.html')

@role_required(['USER'])
def user_notifications(request):
    return render(request, 'User/user_notifications.html')

@role_required(['USER'])
def user_prescription(request):
    return render(request, 'User/user_prescription.html')

@role_required(['USER'])
def user_health_record(request):
    return render(request, 'User/user_health_record.html')

@role_required(['USER'])
def user_emergency(request):
    return render(request, 'User/user_emergency.html')

@role_required(['USER'])
def user_faq(request):
    return render(request, 'User/user_faq.html')