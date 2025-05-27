from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required
from .forms import PatientForm, ConsentForm,AppointmentForm, HealthInformationRecordForm
from .models import Patient, IntraoralExamination, AdminLog, CustomUser, Notification
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
import json
from rapidfuzz import fuzz

from django.db.models import Count, Q




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



@role_required(['ADMIN'])
def admin_patient_info_records(request):
    if request.user.role != 'ADMIN':
        return redirect('forbidden')

    filter_option = request.GET.get('filter', '')
    search_query = request.GET.get('search', '').strip()
    show_form = False

    patient_form = PatientForm()
    consent_form = ConsentForm()

    # Step 1: Start with all patients
    patients = Patient.objects.all()

    # Step 2: Apply filter (verified, complete, incomplete)
    if filter_option == 'verified':
        patients = patients.filter(is_verified=True, is_complete=True)
    elif filter_option == 'complete':
        patients = patients.filter(is_verified=False, is_complete=True)
    elif filter_option == 'incomplete':
        patients = patients.filter(is_verified=False, is_complete=False)

    # Step 3: Fuzzy search
    if search_query:
        search_query_lower = search_query.lower()
        filtered = []
        for patient in patients:
            first = patient.first_name.lower()
            last = patient.last_name.lower()
            middle = patient.middle_name.lower() if patient.middle_name else ""

            if (
                fuzz.partial_ratio(first, search_query_lower) > 80 or
                fuzz.partial_ratio(last, search_query_lower) > 80 or
                fuzz.partial_ratio(middle, search_query_lower) > 80
            ):
                filtered.append(patient)
        patients = filtered

    # Handle form logic
    if request.method == 'POST':
        if 'add_record' in request.POST:
            show_form = True
        else:
            patient_form = PatientForm(request.POST, request.FILES)
            consent_form = ConsentForm(request.POST)
            if patient_form.is_valid() and consent_form.is_valid():
                if consent_form.cleaned_data['consent_signed']:
                    patient = patient_form.save(commit=False)
                    patient.is_complete = True
                    patient.is_verified = False
                    patient.save()
                    messages.success(request, "Patient record successfully added.")
                    return redirect('admin_patient_info_records')
                else:
                    consent_form.add_error('consent_signed', 'Consent must be signed before submission.')
            show_form = True

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
    # Gender distribution
    gender_data = Patient.objects.values('sex').annotate(count=Count('id'))
    gender_labels = [entry['sex'] or 'Not Specified' for entry in gender_data]
    gender_values = [entry['count'] for entry in gender_data]

    # Age group bar chart
    age_groups = {
        '0-12': 0,
        '13-19': 0,
        '20-35': 0,
        '36-50': 0,
        '51+': 0
    }
    for patient in Patient.objects.all():
        age = patient.age
        if age <= 12:
            age_groups['0-12'] += 1
        elif age <= 19:
            age_groups['13-19'] += 1
        elif age <= 35:
            age_groups['20-35'] += 1
        elif age <= 50:
            age_groups['36-50'] += 1
        else:
            age_groups['51+'] += 1

    age_labels = list(age_groups.keys())
    age_counts = list(age_groups.values())

    # Religion distribution
    religion_data = Patient.objects.values('religion').annotate(count=Count('id')).order_by('-count')[:5]
    religion_labels = [entry['religion'] or 'Unknown' for entry in religion_data]
    religion_values = [entry['count'] for entry in religion_data]

    # PhilHealth coverage
    has_philhealth = Patient.objects.filter(~Q(philhealth_no=None), ~Q(philhealth_no="")).count()
    no_philhealth = Patient.objects.count() - has_philhealth

    philhealth_labels = ['With PhilHealth', 'Without PhilHealth']
    philhealth_values = [has_philhealth, no_philhealth]

    context = {
        'gender_labels': json.dumps(gender_labels),
        'gender_values': json.dumps(gender_values),
        'age_labels': json.dumps(age_labels),
        'age_values': json.dumps(age_counts),
        'religion_labels': json.dumps(religion_labels),
        'religion_values': json.dumps(religion_values),
        'philhealth_labels': json.dumps(philhealth_labels),
        'philhealth_values': json.dumps(philhealth_values),
    }
    return render(request, 'Admin/admin_analytics.html', context)


@role_required(['ADMIN'])
def admin_system_logs(request):
    system_logs = AdminLog.objects.filter(log_type='SYSTEM').order_by('-timestamp')
    verified_patients = Patient.objects.select_related('synced_user')
    patient_map = {p.synced_user.id: p for p in verified_patients if p.synced_user}

    hir_form = None
    selected_patient = None

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        selected_patient = get_object_or_404(Patient, synced_user=user)

        if 'fill_hir' in request.POST:
            # Admin clicked Fill Up HIR, render empty form
            hir_form = HealthInformationRecordForm(instance=selected_patient)

        elif 'submit_hir' in request.POST:
            # Admin submitted the HIR form
            hir_form = HealthInformationRecordForm(request.POST, request.FILES, instance=selected_patient)

            if hir_form.is_valid():
                hir_form.save()
                selected_patient.is_verified = True
                selected_patient.is_complete = True
                selected_patient.save()

                try:
                    AdminLog.objects.create(
                        admin=request.user,
                        log_type='SYSTEM',
                        action_description=f"Verified new patient '{user.username}' via admin logs",
                        affected_model='Patient',
                        affected_object_id=selected_patient.id,
                        metadata={"user_id": user.id}
                    )
                except Exception as e:
                    print("Error creating AdminLog:", e)
                    messages.error(request, "Failed to log system action.")

                Notification.objects.create(
                    user=user,
                    type='Account',
                    message='Your Health Information Record has been completed and your account has been verified.',
                    redirect_url='/User'
                )

                messages.success(request, f"HIR completed and patient '{user.username}' verified.")
                return redirect('admin_system_logs')
            else:
                messages.error(request, "Please correct the errors in the HIR form.")

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

        # Notification to users
        Notification.objects.create(
            user=user,
            type='Account',
            message='Your account has been successfully verified by the admin.',
            redirect_url='/User'  # optional
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