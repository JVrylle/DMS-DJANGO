from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required
from .forms import PatientInformationRecordForm, AppointmentForm
from .models import Patient, IntraoralExamination,AdminLog, Appointment
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.timezone import now
from datetime import datetime, date, time as time_obj, timedelta


User = get_user_model()


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
    patient = get_object_or_404(Patient, synced_user=request.user)

    edit_id = request.GET.get('edit')
    delete_id = request.GET.get('delete')

    show_walkin_modal = False
    appointment_date = None
    appointment_purpose = None

    # ------------------------
    # Handle Delete Appointment
    # ------------------------
    if delete_id:
        appointment = get_object_or_404(Appointment, id=delete_id, patient=patient)
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully.')
        return redirect('user_appointments')

    # -------------------------------
    # Handle Walk-in Appointment Form
    # -------------------------------
    if request.method == 'POST' and 'walkin_confirm' in request.POST:
        date_str = request.POST.get('date')
        purpose = request.POST.get('purpose')

        try:
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            try:
                appointment_date = datetime.strptime(date_str, '%B %d, %Y').date()
            except ValueError:
                messages.error(request, "Invalid date format.")
                return redirect('user_appointments')

        if appointment_date < datetime.today().date():
            messages.error(request, "You cannot book a walk-in appointment in the past.")
            return redirect('user_appointments')

        if Appointment.objects.filter(patient=patient, date=appointment_date).exists():
            messages.error(request, "You already have an appointment booked on this date.")
            return redirect('user_appointments')

        Appointment.objects.create(
            patient=patient,
            date=appointment_date,
            purpose=purpose,
            address=patient.home_address,
            created_by=request.user,
            status='Pending-Walk-in'
        )
        messages.success(request, "Walk-in appointment added.")
        return redirect('user_appointments')

    # -------------------------------
    # Handle New or Edit Appointment
    # -------------------------------
    if edit_id:
        # Edit Mode
        appointment = get_object_or_404(Appointment, id=edit_id, patient=patient)
        form = AppointmentForm(request.POST or None, instance=appointment, patient=patient)

        if request.method == 'POST' and form.is_valid():
            new_date = form.cleaned_data['date']
            if new_date < datetime.today().date():
                messages.error(request, "You cannot schedule an appointment in the past.")
            elif Appointment.objects.filter(patient=patient, date=new_date).exclude(id=appointment.id).exists():
                messages.error(request, "You already have an appointment on this date.")
            else:
                form.save()
                messages.success(request, 'Appointment updated successfully.')
                return redirect('user_appointments')
    else:
        # Add Mode
        form = AppointmentForm(request.POST or None, patient=patient)

        if request.method == 'POST':
            if form.is_valid():
                new_appointment = form.save(commit=False)
                new_appointment.patient = patient
                new_appointment.created_by = request.user
                new_appointment.address = patient.home_address

                appointment_date = new_appointment.date
                appointment_purpose = new_appointment.purpose

                if appointment_date < datetime.today().date():
                    messages.error(request, "You cannot schedule an appointment in the past.")
                elif Appointment.objects.filter(patient=patient, date=appointment_date).exists():
                    messages.error(request, "You already have an appointment on this date.")
                else:
                    weekday = appointment_date.weekday()
                    max_patients = 18 if weekday == 5 else 6
                    existing_appt_count = Appointment.objects.filter(date=appointment_date).count()

                    if existing_appt_count >= max_patients:
                        show_walkin_modal = True
                    else:
                        new_appointment.status = 'Pending'
                        new_appointment.save()
                        messages.success(request, f"Appointment created successfully for {appointment_date.strftime('%B %d, %Y')}.")
                        return redirect('user_appointments')
            else:
                messages.error(request, "Please correct the errors in the form.")

    # ------------------------
    # Load Existing Appointments
    # ------------------------
    appointments = Appointment.objects.filter(patient=patient).order_by('-date')

    return render(request, 'User/user_appointments.html', {
        'appointments': appointments,
        'form': form,
        'edit_id': edit_id,
        'show_walkin_modal': show_walkin_modal,
        'appointment_date': appointment_date,
        'appointment_purpose': appointment_purpose,
    })




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

        if form.errors:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            for error in form.non_field_errors():
                messages.error(request, error)



        if form.is_valid():
            new_data = form.save(commit=False)

            # Check for existing patient record (excluding self)
            matched_patient = Patient.objects.filter(
                first_name__iexact=new_data.first_name.strip(),
                middle_name__iexact=new_data.middle_name.strip(),
                last_name__iexact=new_data.last_name.strip(),
                # birthdate=new_data.birthdate
                # PLACE EXTRA INFORMATION HERE
            ).exclude(synced_user=request.user).first()

            if matched_patient:
                # ✅ Existing patient — update that record
                matched_patient.synced_user = request.user
                matched_patient.is_complete = True
                matched_patient.is_verified = False

                # Optional: update with submitted form fields
                valid_fields = [
                    'sex',
                    # 'home_address',
                    # 'cel_mobile_no',
                    'email',
                    # 'occupation',
                    'religion', 
                    'nationality',
                    # 'nickname', 'dental_insurance', 'dental_insurance_effective_date',
                    # 'home_no', 'office_no', 'fax_no'
                    # Add more fields as appropriate
                ]

                for field in valid_fields:
                    setattr(matched_patient, field, getattr(new_data, field))

                matched_patient.save()

                AdminLog.objects.create(
                    log_type='SYSTEM',
                    action_description=f"Existing patient '{request.user.username} ({request.user.email})' is requesting account verification.",
                    affected_model='Patient',
                    affected_object_id=matched_patient.id,
                    metadata={
                        'user_id': request.user.id,
                        'matched_patient_id': matched_patient.id,
                        'status': 'Pending admin verification',
                        'submitted_at': str(now())
                    }
                )
                messages.info(request, "Your request is submitted. Admin will verify your account soon.")

            else:
                # ✅ New patient — save new record
                new_data.synced_user = request.user
                new_data.is_complete = False
                new_data.is_verified = False
                new_data.save()

                AdminLog.objects.create(
                    log_type='SYSTEM',
                    action_description=f"New user '{request.user.username} ({request.user.email})' submitted PIR. No existing match found.",
                    affected_model='Patient',
                    metadata={
                        'request_user_id': request.user.id,
                        'status': 'New patient — in-clinic verification required',
                        'submitted_at': str(now())
                    }
                )
                messages.info(request, "Thank you. Please visit the clinic to complete your registration and verification.")

            return redirect('user_health_record')

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









