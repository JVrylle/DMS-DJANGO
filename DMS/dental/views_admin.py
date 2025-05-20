from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required
from .forms import PatientForm, ConsentForm, IntraoralExaminationForm
from .models import Patient, IntraoralExamination, AdminLog, CustomUser
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

User = get_user_model()

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

@role_required(['DENTIST', 'ADMIN'])
def admin_patient_info_records(request):
    if request.user.role != 'ADMIN':
        return redirect('forbidden')

    filter_option = request.GET.get('filter', 'verified')

    if filter_option == 'complete':
        patients = Patient.objects.filter(is_verified=False, is_complete=True)
    elif filter_option == 'incomplete':
        patients = Patient.objects.filter(is_verified=False, is_complete=False)
    else:  # Default: verified
        patients = Patient.objects.filter(is_verified=True, is_complete=True)

    show_form = False
    patient_form = PatientForm()        # Initialize by default
    consent_form = ConsentForm()        # Initialize by default

    if request.method == 'POST':
        if 'add_record' in request.POST:
            show_form = True  # Only show form
        else:
            patient_form = PatientForm(request.POST)
            consent_form = ConsentForm(request.POST)

            if patient_form.is_valid() and consent_form.is_valid():
                if consent_form.cleaned_data['consent_signed']:
                    patient = patient_form.save(commit=False)
                    patient.is_complete = True
                    patient.is_verified = False
                    patient.save()
                    print(f"Saved patient: {patient.first_name} {patient.last_name}")
                    messages.success(request, "Patient record successfully added.")
                    return redirect('admin_patient_info_records')
                else:
                    consent_form.add_error('consent_signed', 'Consent must be signed before submission.')
            show_form = True  # Form is invalid, so show again

    context = {
        'patients': patients,
        'patient_form': patient_form,
        'consent_form': consent_form,
        'show_form': show_form,
        'filter_option': filter_option,
    }
    return render(request, 'Admin/admin_patient_info_records.html', context)




@role_required(['DENTIST','ADMIN'])
def admin_analytics(request):
    return render(request, 'Admin/admin_analytics.html')

@role_required(['DENTIST','ADMIN'])
def admin_system_logs(request):
    system_logs = AdminLog.objects.filter(log_type='SYSTEM').order_by('-timestamp')
    verified_patients = Patient.objects.select_related('synced_user')

    # Dictionary for easy lookup in template
    patient_map = {p.synced_user.id: p for p in verified_patients if p.synced_user}

    return render(request, 'Admin/admin_system_logs.html', {
        'system_logs': system_logs,
        'patients': patient_map,
    })

@require_POST
@role_required(['ADMIN'])
def verify_patient_from_log(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    patient = Patient.objects.filter(synced_user=user).first()

    if patient:
        patient.is_verified = True
        patient.save()

        AdminLog.objects.create(
            admin=request.user,
            log_type='SYSTEM',
            action_description=f"Admin '{request.user.username}' verified patient account for user '{user.username}'.",
            affected_model='Patient',
            affected_object_id=patient.id,
            metadata={"user_id": user.id}
        )

        messages.success(request, f"Patient '{user.username}' has been verified.")
    else:
        messages.error(request, "Patient record not found.")

    return redirect('admin_system_logs')



@role_required(['DENTIST','ADMIN'])
def admin_security_logs(request):
    return render(request, 'Admin/admin_security_logs.html')

@role_required(['DENTIST','ADMIN'])
def admin_event_logs(request):
    return render(request, 'Admin/admin_event_logs.html')

@role_required(['DENTIST','ADMIN'])
def admin_emergency_logs(request):
    return render(request, 'Admin/admin_emergency_logs.html')