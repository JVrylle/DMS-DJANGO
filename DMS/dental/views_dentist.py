from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required
from .forms import  IntraoralExaminationForm, TreatmentRecordForm
from .models import Patient, IntraoralExamination, TreatmentRecord
import json


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

@role_required(['DENTIST'])
def dentist_patient_health_records(request):
    if request.user.role != 'DENTIST':
        return redirect('forbidden')

    patients = Patient.objects.all()
    selected_patient = None
    intraoral_form = None
    treatment_form = None
    treatment_records = None
    message = None
    show_patient_details = False  # Default
    show_treatment_table = False
    viewing_intraoral = False

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        selected_patient = get_object_or_404(Patient, id=patient_id)


        # Button clicked: View Record
        if 'view_record' in request.POST:
            selected_patient = get_object_or_404(Patient, id=patient_id)
            show_patient_details = True  # Only show details when View Record is clicked
            

        # Button clicked: Fill Intraoral Exam
        elif 'select_patient' in request.POST:
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

                # Save the teeth JSON from the hidden field
                teeth_json = request.POST.get('teeth_json')
                if teeth_json:
                    exam.teeth = json.loads(teeth_json)
                exam.save()
                message = "Intraoral examination submitted successfully."
                intraoral_form = None
                selected_patient = None


        # Button clicked: View Intraoral
        elif 'view_intraoral' in request.POST:
            selected_patient = get_object_or_404(Patient, id=patient_id)
            existing_exam = IntraoralExamination.objects.filter(patient=selected_patient).first()
            if existing_exam:
                intraoral_form = IntraoralExaminationForm(instance=existing_exam)
            else:
                intraoral_form = IntraoralExaminationForm()
            
            viewing_intraoral = True  # New flag

        # Button clicked: View Treatment    
        elif 'view_treatment' in request.POST:
            treatment_records = TreatmentRecord.objects.filter(patient=selected_patient)
            show_treatment_table = True  

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
        'treatment_records': treatment_records,
        'message': message,
        'show_patient_details': show_patient_details, 
        'show_treatment_table': show_treatment_table,
        'viewing_intraoral': viewing_intraoral,
        'row1_left': [51, 52, 53, 54, 55],
        'row1_right': [61, 62, 63, 64, 65],
        'row2_left': [11, 12, 13, 14, 15, 16, 17, 18],
        'row2_right': [21, 22, 23, 24, 25, 26, 27, 28],
        'row3_left': [41, 42, 43, 44, 45, 46, 47, 48],
        'row3_right': [31, 32, 33, 34, 35, 36, 37, 38],
        'row4_left': [81, 82, 83, 84, 85],
        'row4_right': [71, 72, 73, 74, 75],
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
