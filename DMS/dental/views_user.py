from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required
from .forms import PatientForm, ConsentForm, IntraoralExaminationForm, PatientInformationRecordForm
from .models import Patient, IntraoralExamination


# USER
@role_required(['USER'])
def user_dash(request):
    
    #SIDEBAR
    username = request.user.username
    context = {
        'username':username,
    }


    return render(request, 'User/user_dash.html', context)

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
    try:
        patient = Patient.objects.get(synced_user=request.user)
    except Patient.DoesNotExist:
        patient = None

    if request.method == 'POST':
        form = PatientInformationRecordForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.synced_user = request.user
            patient.save()
            return redirect('user_health_record')  # redirect to see submitted data

    else:
        form = PatientInformationRecordForm(instance=patient)

    return render(request, 'User/user_health_record.html', {
        'form': form,
        'patient': patient
    })



@role_required(['USER'])
def user_emergency(request):
    return render(request, 'User/user_emergency.html')

@role_required(['USER'])
def user_faq(request):
    return render(request, 'User/user_faq.html')









