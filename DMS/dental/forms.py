from django import forms
from .models import Patient, IntraoralExamination, TreatmentRecord, CustomUser
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django import forms
from .models import Appointment
from django.core.exceptions import ValidationError
from datetime import datetime, date, time as time_obj
from django.core.exceptions import ValidationError


yes_no = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]

allergies = [
    ('Local Anesthetic', 'Local Anesthetic (e.g., Lidocaine)'),
    ('Penicillin, Antibiotics', 'Penicillin, Antibiotics'),
    ('Sulfa Drugs', 'Sulfa Drugs'),
    ('Aspirin', 'Aspirin'),
    ('Latex', 'Latex'),
    ('Others', 'Others')
]

diseases = [
    ('High Blood Pressure', 'High Blood Pressure'),
    ('Low Blood Pressure', 'Low Blood Pressure'),
    ('Epilepsy/Convulsions', 'Epilepsy / Convulsions'),
    ('AIDS or HIV Infection', 'AIDS or HIV Infection'),
    ('Sexually Transmitted Disease', 'Sexually Transmitted Disease'),
    ('Stomach Troubles / Ulcers', 'Stomach Troubles / Ulcers'),
    ('Fainting Seizures', 'Fainting Seizures'),
    ('Rapid Weight Loss', 'Rapid Weight Loss'),
    ('Radiation Therapy', 'Radiation Therapy'),
    ('Joint Replacement / Implant', 'Joint Replacement / Implant'),
    ('Heart Surgery', 'Heart Surgery'),
    ('Heart Attack', 'Heart Attack'),
    ('Thyroid Problem', 'Thyroid Problem'),
    ('Heart Disease', 'Heart Disease'),
    ('Heart Murmur', 'Heart Murmur'),
    ('Hepatitis / Liver Disease', 'Hepatitis / Liver Disease'),
    ('Rheumatic Fever', 'Rheumatic Fever'),
    ('Hay Fever / Allergies', 'Hay Fever / Allergies'),
    ('Respiratory Problems', 'Respiratory Problems'),
    ('Hepatitis / Jaundice', 'Hepatitis / Jaundice'),
    ('Tuberculosis', 'Tuberculosis'),
    ('Swollen Ankles', 'Swollen Ankles'),
    ('Kidney Disease', 'Kidney Disease'),
    ('Diabetes', 'Diabetes'),
    ('Chest Pain', 'Chest Pain'),
    ('Stroke', 'Stroke'),
    ('Cancer / Tumors', 'Cancer / Tumors'),
    ('Anemia', 'Anemia'),
    ('Angina', 'Angina'),
    ('Asthma', 'Asthma'),
    ('Emphysema', 'Emphysema'),
    ('Bleeding Problems', 'Bleeding Problems'),
    ('Blood Diseases', 'Blood Diseases'),
    ('Head Injuries', 'Head Injuries'),
    ('Arthritis / Rheumatism', 'Arthritis / Rheumatism'),
]




class PatientInformationRecordForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'last_name', 'first_name', 'middle_name', 'nickname',
            'birthdate', 'age', 'sex', 'religion', 'nationality',
            'home_address', 'occupation','philhealth_no', 'dental_insurance',
            'dental_insurance_effective_date',
            'for_minors_parent_or_guardian_name',
            'for_minors_parent_or_guardian_occupation',
            'home_no', 'office_no', 'fax_no', 'cel_mobile_no', 'email',
            'referral_thanks', 'dental_consultation_reason',
        ]


        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'dental_insurance_effective_date': forms.DateInput(attrs={'type': 'date'}),
        }


        
    def __init__(self, *args, **kwargs):
        super(PatientInformationRecordForm, self).__init__(*args, **kwargs)
        
        # Define custom labels for your fields
        custom_labels = {
            'last_name': 'Last Name',
            'first_name': 'First Name',
            'middle_name': 'Middle Name',
            'nickname': 'Nickname',
            'birthdate': 'Date of Birth',
            'age': 'Age',
            'sex': 'Sex',
            'religion': 'Religion',
            'nationality': 'Nationality',
            'home_address': 'Home Address',
            'occupation': 'Occupation',
            'philhealth_no': 'PhilHealth No.',
            'dental_insurance': 'Dental Insurance Provider',
            'dental_insurance_effective_date': 'Insurance Effective Date',
            'for_minors_parent_or_guardian_name': 'For Minors: Parent/Guardian Name',
            'for_minors_parent_or_guardian_occupation': 'For Minors: Parent/Guardian Occupation',
            'home_no': 'Home Phone Number',
            'office_no': 'Office Phone Number',
            'fax_no': 'Fax Number',
            'cel_mobile_no': 'Mobile Number',
            'email': 'Email Address',
            'referral_thanks': 'Whom may we thank for referring you?',
            'dental_consultation_reason': 'What is your reason for dental consultation?',

        }

        #  Apply the custom labels
        for field_name, label in custom_labels.items():
            if field_name in self.fields:
                self.fields[field_name].label = label




class HealthInformationRecordForm(forms.ModelForm):
    mi_is_allergic = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=Patient.allergies,
        label='Allergies (Check all that apply)'
    )

    mi_select_disease = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=Patient.diseases,
        label='Do you have or have you had any of the following?'
    )




    class Meta:
        model = Patient
        fields = [
                  'prev_dentist',
                  'last_dental_visit',
                  'physician_name',
                  'physician_specialty',
                  'physician_office_address',
                  'physician_office_no',
                  'mi_isgoodhealth',
                  'mi_is_under_medical_treatment',
                  'mi_is_under_medical_treatment_followup',
                  'mi_is_serious_illness',
                  'mi_is_serious_illness_followup',
                  'mi_is_hospitalized',
                  'mi_is_hospitalized_followup',
                  'mi_is_taking_prescription',
                  'mi_is_taking_prescription_followup',
                  'mi_is_using_tobacco',
                  'mi_is_using_dangerous_drugs',
                  'mi_is_allergic',
                  'mi_is_allergic_others',
                  'mi_bleeding_time',
                  'mi_is_pregnant',
                  'mi_is_nursing',
                  'mi_is_birth_control',
                  'mi_bloodtype',
                  'mi_bloodpressure',
                  'mi_select_disease',
                  'mi_select_disease_others',
                  'digital_xrays',                 
                  'patient_pictures',              
                  'patient_signatures',     
        ]

        help_texts = {
            'mi_isgoodhealth': 'Select "Yes" if you consider yourself to be in good general health.',
            'mi_is_under_medical_treatment': 'Select "Yes" if you are currently undergoing any kind of medical treatment.',
            'mi_is_under_medical_treatment_followup': 'Please provide details about the treatment you are currently receiving.',
            'mi_is_serious_illness': 'Select "Yes" if you have had any serious illness in the past.',
            'mi_is_serious_illness_followup': 'Mention the type of illness and any treatment received.',
            'mi_is_hospitalized': 'Select "Yes" if you have been hospitalized recently.',
            'mi_is_hospitalized_followup': 'State the reason for hospitalization and the date if possible.',
            'mi_is_taking_prescription': 'Select "Yes" if you are currently taking any prescription medications.',
            'mi_is_taking_prescription_followup': 'List all the prescription medications you are taking.',
            'mi_is_using_tobacco': 'Select "Yes" if you use tobacco products such as cigarettes or chewing tobacco.',
            'mi_is_using_dangerous_drugs': 'Select "Yes" if you are using or have used any dangerous drugs or substances.',
            'mi_is_allergic': 'Select "Yes" if you are allergic to any medication, food, or other substances.',
            'mi_is_allergic_others': 'List any other allergies not mentioned in the choices above.',
            'mi_bleeding_time': 'Enter your average bleeding time (e.g., for minor cuts). Useful for assessing clotting issues.',
            'mi_is_pregnant': 'Select "Yes" if you are currently pregnant.',
            'mi_is_nursing': 'Select "Yes" if you are currently breastfeeding.',
            'mi_is_birth_control': 'Select "Yes" if you are currently using any form of birth control.',
            'mi_bloodtype': 'Enter your blood type if known (e.g., A+, O-, etc.).',
            'mi_bloodpressure': 'Enter your usual blood pressure reading (e.g., 120/80).',
            'mi_select_disease': 'Check any of the listed diseases or conditions that you have had or currently have.',
            'mi_select_disease_others': 'List any diseases or conditions not covered in the options above.',
        }


        widgets = {
            'last_dental_visit': forms.DateInput(attrs={'type': 'date'}),
        }


    def __init__(self, *args, **kwargs):
        super(HealthInformationRecordForm, self).__init__(*args, **kwargs)
        self.fields['mi_is_allergic'].initial = self.instance.mi_is_allergic or []
        self.fields['mi_select_disease'].initial = self.instance.mi_select_disease or []

        custom_labels = {
            'prev_dentist': 'Previous Dentist: Dr.',
            'last_dental_visit': 'Last Dental visit',
            'physician_name': 'Physician Name',
            'physician_specialty': 'Physician Specialty',
            'physician_office_address': 'Physician Office Address:',
            'physician_office_no':'Physician Office Number:',
            'mi_isgoodhealth': 'Are you in good health?',
            'mi_is_under_medical_treatment': 'Under medical treatment?',
            'mi_is_under_medical_treatment_followup': 'If yes, explain',
            'mi_is_serious_illness': 'Any serious illness?',
            'mi_is_serious_illness_followup': 'If yes, explain',
            'mi_is_hospitalized': 'Have you been hospitalized?',
            'mi_is_hospitalized_followup': 'If yes, explain',
            'mi_is_taking_prescription': 'Taking any prescriptions?',
            'mi_is_taking_prescription_followup': 'If yes, explain',
            'mi_is_using_tobacco': 'Do you use tobacco products?',
            'mi_is_using_dangerous_drugs': 'Do you use alcohol, cocaine, or other dangerous drugs?',
            'mi_is_allergic': 'Allergies (Check all that apply)',
            'mi_is_allergic_others': 'Other allergies (if any)',
            'mi_bleeding_time': 'Bleeding Time',
            'mi_is_pregnant': 'For Women: Are you pregnant?',
            'mi_is_nursing': 'Are you nursing?',
            'mi_is_birth_control': 'Using birth control?',
            'mi_bloodtype': 'Blood Type',
            'mi_bloodpressure': 'Blood Pressure',
            'mi_select_disease':'Do you have or have you had any of the following? Check which apply.' ,
            'mi_select_disease_others':'Other Disease:', 
        }

        #  Apply the custom labels
        for field_name, label in custom_labels.items():
            if field_name in self.fields:
                self.fields[field_name].label = label







class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['last_name',
                  'first_name',
                  'middle_name',
                  'nickname',
                  'birthdate',
                  'age',
                  'sex',
                  'religion',
                  'nationality',
                  'home_address',
                  'occupation',
                  'philhealth_no',
                  'dental_insurance',
                  'dental_insurance_effective_date',
                  'for_minors_parent_or_guardian_name',
                  'for_minors_parent_or_guardian_occupation',
                  'home_no',
                  'office_no',
                  'fax_no',
                  'cel_mobile_no',
                  'email',
                  'referral_thanks',
                  'dental_consultation_reason',
                  'prev_dentist',
                  'last_dental_visit',
                  'physician_name',
                  'physician_specialty',
                  'physician_office_address',
                  'physician_office_no',
                  'mi_isgoodhealth',
                  'mi_is_under_medical_treatment',
                  'mi_is_under_medical_treatment_followup',
                  'mi_is_serious_illness',
                  'mi_is_serious_illness_followup',
                  'mi_is_hospitalized',
                  'mi_is_hospitalized_followup',
                  'mi_is_taking_prescription',
                  'mi_is_taking_prescription_followup',
                  'mi_is_using_tobacco',
                  'mi_is_using_dangerous_drugs',
                  'mi_is_allergic',
                  'mi_is_allergic_others',
                  'mi_bleeding_time',
                  'mi_is_pregnant',
                  'mi_is_nursing',
                  'mi_is_birth_control',
                  'mi_bloodtype',
                  'mi_bloodpressure',
                  'mi_select_disease',
                  'mi_select_disease_others',

            'digital_xrays',                
            'patient_pictures',            
            'patient_signatures',      
                  ]

        help_texts = {
            'mi_isgoodhealth': 'Select "Yes" if you consider yourself to be in good general health.',
            'mi_is_under_medical_treatment': 'Select "Yes" if you are currently undergoing any kind of medical treatment.',
            'mi_is_under_medical_treatment_followup': 'Please provide details about the treatment you are currently receiving.',
            'mi_is_serious_illness': 'Select "Yes" if you have had any serious illness in the past.',
            'mi_is_serious_illness_followup': 'Mention the type of illness and any treatment received.',
            'mi_is_hospitalized': 'Select "Yes" if you have been hospitalized recently.',
            'mi_is_hospitalized_followup': 'State the reason for hospitalization and the date if possible.',
            'mi_is_taking_prescription': 'Select "Yes" if you are currently taking any prescription medications.',
            'mi_is_taking_prescription_followup': 'List all the prescription medications you are taking.',
            'mi_is_using_tobacco': 'Select "Yes" if you use tobacco products such as cigarettes or chewing tobacco.',
            'mi_is_using_dangerous_drugs': 'Select "Yes" if you are using or have used any dangerous drugs or substances.',
            'mi_is_allergic': 'Select "Yes" if you are allergic to any medication, food, or other substances.',
            'mi_is_allergic_others': 'List any other allergies not mentioned in the choices above.',
            'mi_bleeding_time': 'Enter your average bleeding time (e.g., for minor cuts). Useful for assessing clotting issues.',
            'mi_is_pregnant': 'Select "Yes" if you are currently pregnant.',
            'mi_is_nursing': 'Select "Yes" if you are currently breastfeeding.',
            'mi_is_birth_control': 'Select "Yes" if you are currently using any form of birth control.',
            'mi_bloodtype': 'Enter your blood type if known (e.g., A+, O-, etc.).',
            'mi_bloodpressure': 'Enter your usual blood pressure reading (e.g., 120/80).',
            'mi_select_disease': 'Check any of the listed diseases or conditions that you have had or currently have.',
            'mi_select_disease_others': 'List any diseases or conditions not covered in the options above.',
        }
        

        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'dental_insurance_effective_date': forms.DateInput(attrs={'type': 'date'}),
            'last_dental_visit': forms.DateInput(attrs={'type': 'date'}),
            
            # 'sex': forms.RadioSelect(),
            # 'mi_isgoodhealth': forms.RadioSelect(),
            # 'mi_is_under_medical_treatment': forms.RadioSelect(),
            # 'mi_is_serious_illness': forms.RadioSelect(),   
            # 'mi_is_hospitalized': forms.RadioSelect(),
            # 'mi_is_taking_prescription': forms.RadioSelect(),
            # 'mi_is_using_tobacco': forms.RadioSelect(),
            # 'mi_is_using_dangerous_drugs': forms.RadioSelect(),
            'mi_is_allergic': forms.CheckboxSelectMultiple(choices=allergies),
            # 'mi_is_pregnant': forms.RadioSelect(),
            # 'mi_is_nursing': forms.RadioSelect(),
            # 'mi_is_birth_control': forms.RadioSelect(),
            'mi_select_disease':forms.CheckboxSelectMultiple(choices=diseases),
        }


    def clean(self):
        cleaned_data = super().clean()
        birthdate = cleaned_data.get('birthdate')
        age = cleaned_data.get('age')

        if birthdate and age is not None:
            today = date.today()
            calculated_age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            
            if age != calculated_age:
                raise ValidationError(f"Age does not match the birthdate. Calculated age is {calculated_age}.")



    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        
        # Define custom labels for your fields
        custom_labels = {
            'last_name': 'Last Name',
            'first_name': 'First Name',
            'middle_name': 'Middle Name',
            'nickname': 'Nickname',
            'birthdate': 'Date of Birth',
            'age': 'Age',
            'sex': 'Sex',
            'religion': 'Religion',
            'nationality': 'Nationality',
            'home_address': 'Home Address',
            'occupation': 'Occupation',
            'philhealth_no': 'PhilHealth No.',
            'dental_insurance': 'Dental Insurance Provider',
            'dental_insurance_effective_date': 'Insurance Effective Date',
            'for_minors_parent_or_guardian_name': 'For Minors: Parent/Guardian Name',
            'for_minors_parent_or_guardian_occupation': 'For Minors: Parent/Guardian Occupation',
            'home_no': 'Home Phone Number',
            'office_no': 'Office Phone Number',
            'fax_no': 'Fax Number',
            'cel_mobile_no': 'Mobile Number',
            'email': 'Email Address',
            'referral_thanks': 'Whom may we thank for referring you?',
            'dental_consultation_reason': 'What is your reason for dental consultation?',
            'prev_dentist': 'Previous Dentist: Dr.',
            'last_dental_visit': 'Last Dental visit',
            'physician_name': 'Physician Name',
            'physician_specialty': 'Physician Specialty',
            'physician_office_address': 'Physician Office Address:',
            'physician_office_no':'Physician Office Number:',
            'mi_isgoodhealth': 'Are you in good health?',
            'mi_is_under_medical_treatment': 'Under medical treatment?',
            'mi_is_under_medical_treatment_followup': 'If yes, explain',
            'mi_is_serious_illness': 'Any serious illness?',
            'mi_is_serious_illness_followup': 'If yes, explain',
            'mi_is_hospitalized': 'Have you been hospitalized?',
            'mi_is_hospitalized_followup': 'If yes, explain',
            'mi_is_taking_prescription': 'Taking any prescriptions?',
            'mi_is_taking_prescription_followup': 'If yes, explain',
            'mi_is_using_tobacco': 'Do you use tobacco products?',
            'mi_is_using_dangerous_drugs': 'Do you use alcohol, cocaine, or other dangerous drugs?',
            'mi_is_allergic': 'Allergies (Check all that apply)',
            'mi_is_allergic_others': 'Other allergies (if any)',
            'mi_bleeding_time': 'Bleeding Time',
            'mi_is_pregnant': 'For Women: Are you pregnant?',
            'mi_is_nursing': 'Are you nursing?',
            'mi_is_birth_control': 'Using birth control?',
            'mi_bloodtype': 'Blood Type',
            'mi_bloodpressure': 'Blood Pressure',
            'mi_select_disease':'Do you have or have you had any of the following? Check which apply.' ,
            'mi_select_disease_others':'Other Disease:', 
        }

        #  Apply the custom labels
        for field_name, label in custom_labels.items():
            if field_name in self.fields:
                self.fields[field_name].label = label







class ConsentForm(forms.Form):
    consent_signed = forms.BooleanField(label="Patient has signed digital informed consent.")



class IntraoralExaminationForm(forms.ModelForm):
    class Meta:
        model = IntraoralExamination
        fields = [
            'xray_taken',
            'xray_periapical',
            'xray_taken_others',
            'periodontal_screening',
            'occlusion',
            'appliances',
            'appliances_others',
            'tmd',
                  ]

        xray_choices = [
            ('PERIAPICAL','Periapical'),
            ('PANORAMIC','Panoramic'),
            ('CEPHALOMETRIC','Cephalometric'),
            ('OCCLUSAL (UPPER/LOWER)','Occlusal (Upper/Lower)'),
        ]

        periodontal_choices = [
            ('GINGIVITIS','Gingivitis'),
            ('EARLY PERIODONTITIS','Early Periodontitis'),
            ('MODERATE PERIODONTITIS','Moderate Periodontitis'),
            ('ADVANCED PERIODONTITIS','Advanced Periodontitis'),
        ]

        occlusion_choices = [
            ('CLASS (MOLAR)','Class (Molar)'),
            ('OVERJET','Overjet'),
            ('OVERBITE','Overbite'),
            ('MIDLINE DEVIATION','Midline Deviation'),
            ('CROSSBITE','Crossbite'),
        ]


        appliances_choices = [
            ('ORTHODONTIC','Orthodontic'),
            ('STAYPLATE','Stayplate'),
        ]

        tmd_choices = [
            ('CLENCHING','Clenching'),
            ('CLICKING','Clicking'),
            ('TRISMUS','Trismus'),
            ('MUSCLE SPASM','Muscle Spasm'),
        ]

        widgets = {
            'xray_taken': forms.CheckboxSelectMultiple(choices=xray_choices),
            'periodontal_screening' : forms.CheckboxSelectMultiple(choices=periodontal_choices),
            'occlusion' : forms.CheckboxSelectMultiple(choices=occlusion_choices),
            'appliances' : forms.CheckboxSelectMultiple(choices=appliances_choices),
            'tmd' : forms.CheckboxSelectMultiple(choices=tmd_choices),
        }

    def __init__(self, *args, **kwargs):
        super(IntraoralExaminationForm, self).__init__(*args, **kwargs)
        
        # Define custom labels for your fields
        custom_labels = {
            'xray_taken':'X-ray Taken: ',
            'xray_periapical':'Periapical (Tth Number:)',
            'xray_taken_others':'Other X-rays: ',
            'periodontal_screening':'Periodontal Screening: ',
            'occlusion':'Occlusion: ',
            'appliances':'Applicances: ',
            'appliances_others':'Other Appliances: ',
            'tmd':'TMD: ',
        }

        #  Apply the custom labels
        for field_name, label in custom_labels.items():
            if field_name in self.fields:
                self.fields[field_name].label = label

class TreatmentRecordForm(forms.ModelForm):
    class Meta:
        model = TreatmentRecord
        fields = [
            # 'treatment_date',
            'tooth_number',
            'treatment_procedure',
            'treatment_dentist',
            'amount_charged',
            'amount_paid',
            'balance',
            'next_appointment'
        ]
        widgets = {
            # 'treatment_date': forms.DateInput(attrs={'type': 'date'}),
            'next_appointment': forms.DateInput(attrs={'type': 'date'}),
        }


















class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        # Validate password strength
        validate_password(password1)

        return password2

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("Username is required.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.role = 'USER'
        if commit:
            user.save()
        return user

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'purpose']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        date_ = cleaned_data.get('date')

        if date_:
            if date_ < date.today():
                raise ValidationError("Appointment date cannot be in the past.")
            if date_.weekday() == 6:
                raise ValidationError("The clinic is closed on Sundays.")

            # Prevent duplicate booking by same patient on same date
            conflict = Appointment.objects.filter(
                patient=self.patient,
                date=date_
            )
            if self.instance.pk:
                conflict = conflict.exclude(pk=self.instance.pk)

            if conflict.exists():
                raise ValidationError("You already have an appointment on this day.")
