from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required
from .forms import PatientForm, ConsentForm, IntraoralExaminationForm
from .models import Patient, IntraoralExamination


# ADMIN
@role_required(['DENTIST','ADMIN'])
def admin_dash(request):
    #SIDEBAR
    username = request.user.username
    context = {
        'username':username,
    }

    return render(request, 'Admin/admin_dash.html', context)

@role_required(['DENTIST','ADMIN'])
def admin_appointments(request):
    return render(request, 'Admin/admin_appointments.html')

@role_required(['DENTIST','ADMIN'])
def admin_patient_info_records(request):

    ### ADD PATIENT INFORMATION TO DATABASE
    if request.user.role != 'ADMIN':
        return redirect('forbidden')  # Optional: Handle forbidden access

    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        consent_form = ConsentForm(request.POST)

        if patient_form.is_valid() and consent_form.is_valid():
            if consent_form.cleaned_data['consent_signed']:
                patient = patient_form.save()
                print(f"Saved patient: {patient.first_name} {patient.last_name}")
                return redirect('admin_dash')  # Redirect to dashboard or success page
            else:
                consent_form.add_error('consent_signed', 'Consent must be signed before submission.')

    else:
        patient_form = PatientForm()
        consent_form = ConsentForm()

    context = {
        'patient_form': patient_form,
        'consent_form': consent_form,
    }
    return render(request, 'Admin/admin_patient_info_records.html', context)




@role_required(['DENTIST','ADMIN'])
def admin_analytics(request):
    return render(request, 'Admin/admin_analytics.html')

@role_required(['DENTIST','ADMIN'])
def admin_system_logs(request):
    return render(request, 'Admin/admin_system_logs.html')

@role_required(['DENTIST','ADMIN'])
def admin_security_logs(request):
    return render(request, 'Admin/admin_security_logs.html')

@role_required(['DENTIST','ADMIN'])
def admin_event_logs(request):
    return render(request, 'Admin/admin_event_logs.html')

@role_required(['DENTIST','ADMIN'])
def admin_emergency_logs(request):
    return render(request, 'Admin/admin_emergency_logs.html')