from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required
from .forms import PatientForm, ConsentForm, IntraoralExaminationForm
from .models import Patient, IntraoralExamination


# DENTIST
@role_required(['DENTIST'])
def dentist_dash(request):
    #SIDEBAR
    username = request.user.username
    context = {
        'username':username,
    }

    return render(request, 'Dentist/dentist_dash.html', context)

@role_required(['DENTIST'])
def dentist_appointments(request):
    return render(request, 'Dentist/dentist_appointments.html')

@role_required(['DENTIST'])
def dentist_patient_info_record(request):
    return render(request, 'Dentist/dentist_patient_info.html')

# @role_required(['DENTIST'])
# def dentist_patient_health_records(request):

#     if request.user.role != 'ADMIN':
#         return redirect('forbidden')  # Optional: Handle forbidden access

#     patients = Patient.objects.all()

#     context = {
#         'patients': patients,
#     }
#     return render(request, 'Dentist/dentist_patient_health_records.html', context)

@role_required(['DENTIST'])
def dentist_patient_health_records(request):
    if request.user.role != 'DENTIST':
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




@role_required(['DENTIST'])
def dentist_analytics(request):
    return render(request, 'Dentist/dentist_analytics.html')

@role_required(['DENTIST'])
def dentist_notifications(request):
    return render(request, 'Dentist/dentist_notifications.html')

@role_required(['DENTIST'])
def dentist_give_prescription(request):
    return render(request, 'Dentist/dentist_give_prescription.html')

@role_required(['DENTIST'])
def dentist_emergency(request):
    return render(request, 'Dentist/dentist_emergency.html')

@role_required(['DENTIST'])
def dentist_faq(request):
    return render(request, 'Dentist/dentist_faq.html')
