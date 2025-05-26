from django.shortcuts import render, redirect, get_object_or_404
from .decorators import role_required
from .forms import PatientInformationRecordForm, AppointmentForm
from .models import Patient,AdminLog, Appointment, Notification
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.timezone import now
from datetime import datetime, time as time_obj
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



User = get_user_model()


@role_required(['USER'])
def user_dash(request):
    user = request.user

    if request.method == 'POST' and request.POST.get('notification_id'):
        notification_id = request.POST.get('notification_id')
        try:
            notification = Notification.objects.get(id=notification_id, user=user)
            notification.is_read = True
            notification.save()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)

    # For GET requests — normal page load
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)

    context = {
        'username': user.username,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
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

    # if request.GET.get('fetch') == 'calendar':
    #     # Return appointment events for FullCalendar
    #     events = [
    #     {
    #         "title": "John Doe",
    #         "start": "2025-05-25T17:00:00",
    #         "end": "2025-05-25T17:30:00",
    #     },
    #     # Add more events here
    #     ]
    #     return JsonResponse(events, safe=False)

    if request.GET.get('fetch') == 'calendar':
        appointments = Appointment.objects.filter(patient=patient)

        events = []
        for appt in appointments:
            start_datetime = f"{appt.date}T17:00:00"  # adjust time if needed
            end_datetime = f"{appt.date}T17:30:00"    # simple 30 min duration

            events.append({
                "title": f"{appt.purpose} ({appt.status})",
                "start": start_datetime,
                "end": end_datetime,
                "color": (
                    "#22c55e" if appt.status == "Approved" else
                    "#facc15" if appt.status.startswith("Pending") else
                    "#ef4444" if appt.status == "Rejected" else
                    "#3b82f6"  # default blue
                )
            })

        return JsonResponse(events, safe=False)
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

    purpose_descriptions = {
        'Oral Exam': 'Basic dental check-up to assess the patient’s oral health.',
        'Oral Propelaxis': 'Cleaning and polishing of teeth to remove plaque and tartar.',
        'Tooth Restoration': 'Filling cavities and restoring damaged teeth.',
        'Tooth Extraction': 'Removal of decayed or problematic teeth.',
        'Orthodontic Treatment': 'Braces or other treatments to correct teeth alignment.',
        'Minor Surgical Treatment': 'Small surgical procedures like gum surgery.',
        'Fluoride Application': 'Application of fluoride for strengthening enamel.',
        'Prosthodontic Treatment': 'Dentures, crowns, bridges to replace missing teeth.',
    }

    context = {
        'appointments': appointments,
        'form': form,
        'edit_id': edit_id,
        'show_walkin_modal': show_walkin_modal,
        'appointment_date': appointment_date,
        'appointment_purpose': appointment_purpose,
        'purpose_descriptions': purpose_descriptions, 
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('User/user_appointments.html', context, request=request)
        return JsonResponse({'html': html, 'banner_title': 'Appointments'})

    return render(request, 'User/user_appointments.html', context)




@role_required(['USER'])
def user_analytics(request):
    return render(request, 'User/user_analytics.html')


@role_required(['USER'])
def user_notifications(request):
    user = request.user

    if request.method == 'POST':
        # Handle AJAX request to mark notification as read
        notif_id = request.POST.get('notification_id')
        try:
            notif = Notification.objects.get(id=notif_id, user=user)
            notif.is_read = True
            notif.save()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)

    # GET request - render page with notifications
    notifications = user.notifications.all().order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)

    return render(request, 'User/user_notifications.html', {
        'notifications': notifications,
        'unread_notifications': unread_notifications
    })

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

            # ✅ Sanitize and check required fields
            first_name = new_data.first_name.strip()
            middle_name = new_data.middle_name.strip()
            last_name = new_data.last_name.strip()
            birthdate = new_data.birthdate

            if not all([first_name, last_name, birthdate]):
                messages.error(request, "First name, Last name, and Birthdate are required.")
                return render(request, 'User/user_health_record.html', {
                    'form': form,
                    'patient': patient
                })

            # ✅ Check for existing patient record (excluding self)
            matched_patient = Patient.objects.filter(
                first_name__iexact=first_name,
                middle_name__iexact=middle_name,
                last_name__iexact=last_name,
                birthdate=birthdate
            ).exclude(synced_user=request.user).first()

            if matched_patient:
                # ✅ Existing patient — update that record
                matched_patient.synced_user = request.user
                matched_patient.is_complete = True
                matched_patient.is_verified = False

                # Optional: update with submitted form fields
                valid_fields = [
                    'sex',
                    'email',
                    'religion', 
                    'nationality',
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
                    action_description=f"New patient '{request.user.username} ({request.user.email})' registered but requires in-clinic verification.",
                    affected_model='Patient',
                    affected_object_id=new_data.id,
                    metadata={
                        'user_id': request.user.id,
                        'new_patient_id': new_data.id,
                        'status': 'Pending clinic visit',
                        'submitted_at': str(now())
                    }
                )
                messages.info(request, "You have been registered. Please visit the clinic to complete your verification.")

            return redirect('user_health_record')

    else:
        form = PatientInformationRecordForm(instance=patient)

    return render(request, 'User/user_health_record.html', {
        'form': form,
        'patient': patient,
        'show_existing_patient_modal': not patient
    })




@role_required(['USER'])
def user_emergency(request):
    return render(request, 'User/user_emergency.html')

@role_required(['USER'])
def user_faq(request):
    return render(request, 'User/user_faq.html')









