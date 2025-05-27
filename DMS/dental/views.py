from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required
from .forms import PatientForm, ConsentForm, IntraoralExaminationForm
from .models import Patient, IntraoralExamination
# from .models import AdminProfile, Patient

# NOTICE IMPOTANT
# Decorators are temporarily disabled for faster development
#
#


# WEBSITE
def website(request):
    return render(request, 'webs.html')

# USER
# @role_required(['USER'])
def user_dash(request):
    return render(request, 'User/user_dash.html')

# @role_required(['USER'])
def user_appointments(request):
    return render(request, 'User/user_appointments.html')

# @role_required(['USER'])
def user_analytics(request):
    return render(request, 'User/user_analytics.html')

# @role_required(['USER'])
def user_notifications(request):
    return render(request, 'User/user_notifications.html')

# @role_required(['USER'])
def user_prescription(request):
    return render(request, 'User/user_prescription.html')

# @role_required(['USER'])
def user_health_record(request):
    return render(request, 'User/user_health_record.html')

# @role_required(['USER'])
def user_emergency(request):
    return render(request, 'User/user_emergency.html')

# @role_required(['USER'])
def user_faq(request):
    return render(request, 'User/user_faq.html')


# DENTIST
# @role_required(['DENTIST','ADMIN'])
def dentist_dash(request):
    return render(request, 'Dentist/dentist_dash.html')

# @role_required(['DENTIST'])
def dentist_appointments(request):
    return render(request, 'Dentist/dentist_appointments.html')

# @role_required(['DENTIST'])
def dentist_patient_info_record(request):
    return render(request, 'Dentist/dentist_patient_info.html')

# # @role_required(['DENTIST'])
# def dentist_patient_health_records(request):

#     if request.user.role != 'ADMIN':
#         return redirect('forbidden')  # Optional: Handle forbidden access

#     patients = Patient.objects.all()

#     context = {
#         'patients': patients,
#     }
#     return render(request, 'Dentist/dentist_patient_health_records.html', context)

# @role_required(['DENTIST'])
def dentist_patient_health_records(request):
    if request.user.role != 'ADMIN':
        return redirect('forbidden')

    patients = Patient.objects.all()
    selected_patient = None
    intraoral_form = IntraoralExaminationForm()
    message = None

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        selected_patient = get_object_or_404(Patient, id=patient_id)

        # Check if this patient already has an intraoral exam
        existing_exam = IntraoralExamination.objects.filter(patient=selected_patient).first()

        if existing_exam:
            intraoral_form = IntraoralExaminationForm(request.POST, instance=existing_exam)
        else:
            intraoral_form = IntraoralExaminationForm(request.POST)

        if intraoral_form.is_valid():
            exam = intraoral_form.save(commit=False)
            exam.patient = selected_patient
            exam.save()
            message = "Intraoral examination submitted successfully."
            intraoral_form = IntraoralExaminationForm()  # Clear form after submission
            return redirect('dentist_patient_health_records')
        else:
            message = "Please correct the form."

    context = {
        'patients': patients,
        'selected_patient': selected_patient,
        'intraoralexamination_form': intraoral_form,
        'message': message,
    }
    return render(request, 'Dentist/dentist_patient_health_records.html', context)




# @role_required(['DENTIST'])
def dentist_analytics(request):
    return render(request, 'Dentist/dentist_analytics.html')

# @role_required(['DENTIST'])
def dentist_notifications(request):
    return render(request, 'Dentist/dentist_notifications.html')

# @role_required(['DENTIST'])
def dentist_give_prescription(request):
    return render(request, 'Dentist/dentist_give_prescription.html')

# @role_required(['DENTIST'])
def dentist_emergency(request):
    return render(request, 'Dentist/dentist_emergency.html')

# @role_required(['DENTIST'])
def dentist_faq(request):
    return render(request, 'Dentist/dentist_faq.html')


# ADMIN
# @role_required(['DENTIST','ADMIN'])
def admin_dash(request):
    return render(request, 'Admin/admin_dash.html')

# @role_required(['DENTIST','ADMIN'])
def admin_appointments(request):
    return render(request, 'Admin/admin_appointments.html')

# @role_required(['DENTIST','ADMIN'])
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




# @role_required(['DENTIST','ADMIN'])
def admin_analytics(request):
    return render(request, 'Admin/admin_analytics.html')

# @role_required(['DENTIST','ADMIN'])
def admin_system_logs(request):
    return render(request, 'Admin/admin_system_logs.html')

# @role_required(['DENTIST','ADMIN'])
def admin_security_logs(request):
    return render(request, 'Admin/admin_security_logs.html')

# @role_required(['DENTIST','ADMIN'])
def admin_event_logs(request):
    return render(request, 'Admin/admin_event_logs.html')

# @role_required(['DENTIST','ADMIN'])
def admin_emergency_logs(request):
    return render(request, 'Admin/admin_emergency_logs.html')




# TESTING
@role_required(['DENTIST','ADMIN'])
def testing(request):
    testing_list = [1,2,3,4,5]

    context = {
        'testing_list': testing_list
    }

    return render(request, 'testing.html', context)

# FORBIDDEN 
def forbidden(request):
    return render(request, 'forbidden.html')




# THIS IS TESTING 
@role_required(['ADMIN'])
def phase1_input_view(request):
    # Admin or assistant can input patient info
    pass

@role_required(['DENTIST'])
def intraoral_exam_view(request):
    # Dentist only
    pass

@role_required(['USER'])
def appointment_crud_view(request):
    # Users manage their appointments
    pass

def dashboard_redirect_view(request):
    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif request.user.role == 'DENTIST':
        return redirect('dentist_dashboard')
    else:
        return redirect('user_dashboard')
