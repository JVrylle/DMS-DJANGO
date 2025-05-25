from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required
from .forms import PatientForm, ConsentForm,AppointmentForm, HealthInformationRecordForm
from .models import Patient, IntraoralExamination, AdminLog, CustomUser
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from .models import Appointment
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime 
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime



User = get_user_model()

# ADMIN
@role_required(['ADMIN'])
def admin_dash(request):
    #SIDEBAR
    username = request.user.username
    context = {
        'username':username,
    }

    return render(request, 'Admin/admin_dash.html', context)

@role_required(['ADMIN'])
def admin_appointments(request):
    if request.GET.get('fetch') == 'calendar':
        # Unified calendar event logic
        appointments = Appointment.objects.select_related('patient').all()

        events = []
        for appt in appointments:
            start_datetime = f"{appt.date}T17:00:00"  # Assuming 5PM default

            events.append({
                "title": f"{appt.patient.first_name} {appt.patient.last_name} - {appt.purpose}",
                "start": start_datetime,
                "color": (
                    "#22c55e" if appt.status == "Approved" else
                    "#facc15" if appt.status.startswith("Pending") else
                    "#ef4444" if appt.status == "Rejected" else
                    "#007bff"  # Default blue for Scheduled
                )
            })

        return JsonResponse(events, safe=False)

    # Below: rest of the logic (pagination, filtering, etc.)
    edit_appt = None
    form = None
    status_filter = request.GET.get('status')
    date_str = request.GET.get('date')
    date_filter = None

    if date_str:
        try:
            date_filter = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            pass

    appointments_qs = Appointment.objects.select_related('patient').all().order_by('-date')

    if status_filter:
        appointments_qs = appointments_qs.filter(status=status_filter)

    if date_filter:
        appointments_qs = appointments_qs.filter(date=date_filter)

    paginator = Paginator(appointments_qs, 10)
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)

    today_appointments = Appointment.objects.select_related('patient')\
        .filter(date=timezone.localdate())\
        .order_by('date')

    if request.method == 'POST':
        action = request.POST.get('action')
        appt_id = request.POST.get('appointment_id')

        if appt_id and action:
            appointment = get_object_or_404(Appointment, id=appt_id)

            if action == 'approve' and appointment.status in ['Pending', 'Pending-Walk-in']:
                appointment.status = 'Approved'
                appointment.save()
            elif action == 'reject' and appointment.status in ['Pending', 'Pending-Walk-in']:
                appointment.status = 'Rejected'
                appointment.save()
            elif action == 'save':
                form = AppointmentForm(request.POST, instance=appointment)
                if form.is_valid():
                    form.save()

            return redirect('admin_appointments')

    if 'edit' in request.GET:
        edit_appt = get_object_or_404(Appointment, id=request.GET.get('edit'))
        form = AppointmentForm(instance=edit_appt)
    elif 'delete' in request.GET:
        appt = get_object_or_404(Appointment, id=request.GET.get('delete'))
        appt.delete()
        return redirect('admin_appointments')

    return render(request, 'Admin/admin_appointments.html', {
        'appointments': appointments,
        'edit_appt': edit_appt,
        'form': form,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'today_appointments': today_appointments,
    })


@role_required([ 'ADMIN'])
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




@role_required(['ADMIN'])
def admin_analytics(request):
    return render(request, 'Admin/admin_analytics.html')

@role_required(['ADMIN'])
def admin_system_logs(request):
    system_logs = AdminLog.objects.filter(log_type='SYSTEM').order_by('-timestamp')
    verified_patients = Patient.objects.select_related('synced_user')
    patient_map = {p.synced_user.id: p for p in verified_patients if p.synced_user}

    hir_form = None
    selected_patient = None

    # 1. Admin clicks "Fill Up HIR"
    if request.method == 'POST' and 'fill_hir' in request.POST:
        user_id = request.POST.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        selected_patient = get_object_or_404(Patient, synced_user=user)
        hir_form = HealthInformationRecordForm(instance=selected_patient)

    # 2. Admin submits filled-out HIR
    elif request.method == 'POST' and 'submit_hir' in request.POST:
        user_id = request.POST.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        selected_patient = get_object_or_404(Patient, synced_user=user)
        hir_form = HealthInformationRecordForm(request.POST, instance=selected_patient)

        if hir_form.is_valid():
            hir_form.save()
            selected_patient.is_verified = True
            selected_patient.is_complete = True
            selected_patient.save()

            AdminLog.objects.create(
                admin=request.user,
                log_type='SYSTEM',
                action_description=f"Admin '{request.user.username}' filled out HIR and verified patient '{user.username}'.",
                affected_model='Patient',
                affected_object_id=selected_patient.id,
                metadata={"user_id": user.id}
            )

            messages.success(request, f"HIR completed and patient '{user.username}' verified.")
            return redirect('admin_system_logs')

    return render(request, 'Admin/admin_system_logs.html', {
        'system_logs': system_logs,
        'patients': patient_map,
        'hir_form': hir_form,
        'selected_patient': selected_patient,
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



@role_required(['ADMIN'])
def admin_security_logs(request):
    return render(request, 'Admin/admin_security_logs.html')

@role_required(['ADMIN'])
def admin_event_logs(request):
    return render(request, 'Admin/admin_event_logs.html')

@role_required(['ADMIN'])
def admin_emergency_logs(request):
    return render(request, 'Admin/admin_emergency_logs.html')