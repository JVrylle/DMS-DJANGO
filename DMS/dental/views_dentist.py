from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required
from .forms import  IntraoralExaminationForm, TreatmentRecordForm
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
#     if request.user.role != 'DENTIST':
#         return redirect('forbidden')

#     patients = Patient.objects.all()
#     selected_patient = None
#     intraoral_form = IntraoralExaminationForm()
#     treatment_form = None
#     message = None

#     if request.method == 'POST':
#         patient_id = request.POST.get('patient_id')
#         selected_patient = get_object_or_404(Patient, id=patient_id)

#         if 'submit_exam' in request.POST:

#             # Check if this patient already has an intraoral exam
#             existing_exam = IntraoralExamination.objects.filter(patient=selected_patient).first()

#             if existing_exam:
#                 intraoral_form = IntraoralExaminationForm(request.POST, instance=existing_exam)
#             else:
#                 intraoral_form = IntraoralExaminationForm(request.POST)

#             if intraoral_form.is_valid():
#                 exam = intraoral_form.save(commit=False)
#                 exam.patient = selected_patient
#                 exam.save()
#                 message = "Intraoral examination submitted successfully."
#                 intraoral_form = IntraoralExaminationForm()  # Clear form after submission
#                 selected_patient = None  # Reset after save
#             else:
#                 message = "Please correct the form."
#         else: 
#             # Just selecting patient — do not submit form
#             existing_exam = IntraoralExamination.objects.filter(patient=selected_patient).first()
#             if existing_exam:
#                 intraoral_form = IntraoralExaminationForm(instance=existing_exam)

#     context = {
#         'patients': patients,
#         'selected_patient': selected_patient,
#         'intraoralexamination_form': intraoral_form,
#         'message': message,
#     }
#     return render(request, 'Dentist/dentist_patient_health_records.html', context)

@role_required(['DENTIST'])
def dentist_patient_health_records(request):
    if request.user.role != 'DENTIST':
        return redirect('forbidden')

    patients = Patient.objects.all()
    selected_patient = None
    intraoral_form = None
    treatment_form = None
    message = None

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        selected_patient = get_object_or_404(Patient, id=patient_id)

        # Button clicked: Fill Intraoral Exam
        if 'select_patient' in request.POST:
            existing_exam = IntraoralExamination.objects.filter(patient=selected_patient).first()
            if existing_exam:
                intraoral_form = IntraoralExaminationForm(instance=existing_exam)
            else:
                intraoral_form = IntraoralExaminationForm()

        # Button clicked: Submit Intraoral Exam
        elif 'submit_exam' in request.POST:
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
                intraoral_form = None
                selected_patient = None

        # Button clicked: Show Treatment Form
        elif 'update_treatment' in request.POST:
            treatment_form = TreatmentRecordForm()

        # Button clicked: Submit Treatment Form
        elif 'submit_treatment' in request.POST:
            treatment_form = TreatmentRecordForm(request.POST)
            if treatment_form.is_valid():
                record = treatment_form.save(commit=False)
                record.patient = selected_patient
                record.save()
                message = "Treatment record saved successfully."
                treatment_form = None
                selected_patient = None

    context = {
        'patients': patients,
        'selected_patient': selected_patient,
        'intraoralexamination_form': intraoral_form,
        'treatment_form': treatment_form,
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
