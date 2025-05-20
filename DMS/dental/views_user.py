from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required
from .forms import PatientForm, ConsentForm, IntraoralExaminationForm, PatientInformationRecordForm
from .models import Patient, IntraoralExamination,AdminLog
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.timezone import now


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









