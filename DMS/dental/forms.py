from django import forms
from .models import Patient, IntraoralExamination, TreatmentRecord, CustomUser

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
                  'mi_is_hospitalized_folloup',
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
                  ]

        sex_choices = [
            ('Male','Male'),
            ('Female','Female'),
        ]

        allergies = [
            ('LOCAL ANESTHETIC','Local Anesthetic (ex. Lidocaine)'),
            ('PENICILIN, ANTIBIOTICS','Penicilin, Antibiotics'),
            ('SULFA DRUGS','Sulfa Drugs'),
            ('ASPIRIN','Aspirin'),
            ('LATEX','Latex'),
            ('OTHERS','Others')
        ]

        yes_no = [
            ('Yes','Yes'),
            ('Yes','No'),
        ]

        diseases = [
            ('HIGH BLOOD PRESSURE','High Blood Pressure'),
            ('LOW BLOOD PRESSURE','Low Blood Pressure'),
            ('EPILEPSY/CONVULSIONS','Epilepsy / Conculsions'),
            ('AIDS OR HIV INFECTION','AIDS or HIV Infection'),
            ('SEXUALLY TRANSMITTED DISEASE','Sexually Transmitted Disease'),
            ('STOMACH TROUBLES / ULCERS','Stomach Troubles / Ulcers'),
            ('FAINTING SEIZURES','Fainting Seizures'),
            ('RAPID WEIGHT LOSS','Rapid Weight Loss'),
            ('RADIATION THERAPY','Radiation Therapy'),
            ('JOINT REPLACEMENT / IMPLANT','Joint Replacement / Implant'),
            ('HEART SURGERY','Heart Surgery'),
            ('HEART ATTACK','Heart Attack'),
            ('THYROID PROBLEM','Thyroid Problem'),
            ('HEART DISEASE','Heart Disease'),
            ('HEART MURMUR','Heart Murmur'),
            ('HEPATITIS / LIVER DISEASE','Hepatitis / Liver Disease'),
            ('RHEUMATIC FEVER','Rheumatic Fever'),
            ('HAY FEVER / ALLERGIES','Hay Fever / Allergies'),
            ('RESPIRATORY PROBLEMS','Respiratory Problems'),
            ('HEPATITIS / JAUNDICE','Hepatitis / Jaundice'),
            ('TUBERCULOSIS','Tuberculosis'),
            ('SWOLLEN ANKLES','Swollen Ankles'),
            ('KIDNEY DISEASE','Kidney Disease'),
            ('DIABETES','Diabetes'),
            ('CHEST PAIN','Chest Pain'),
            ('STROKE','Stroke'),
            ('CANCER / TUMORS','Cancer / Trumors'),
            ('ANEMIA','Anemia'),
            ('ANGINA','Angina'),
            ('ASTHMA','Asthma'),
            ('EMPHYSEMA','Empysema'),
            ('BLEEDING PROBLEMS','Bleeding Problems'),
            ('BLOOD DISEASES','Blood Diseases'),
            ('HEAD INJURIES','Head Injuries'),
            ('ARTHRITIS / RHEUMATISM','Arthritis / Rheumatism'),
        ]

        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'dental_insurance_effective_date': forms.DateInput(attrs={'type': 'date'}),
            'sex': forms.RadioSelect(choices=sex_choices),
            'mi_isgoodhealth': forms.RadioSelect(choices=yes_no),
            'mi_is_under_medical_treatment': forms.RadioSelect(choices=yes_no),
            'mi_is_serious_illness': forms.RadioSelect(choices=yes_no),   
            'mi_is_hospitalized': forms.RadioSelect(choices=yes_no),
            'mi_is_taking_prescription': forms.RadioSelect(choices=yes_no),
            'mi_is_using_tobacco': forms.RadioSelect(choices=yes_no),
            'mi_is_using_dangerous_drugs': forms.RadioSelect(choices=yes_no),
            'mi_is_allergic': forms.CheckboxSelectMultiple(choices=allergies),
            'mi_is_pregnant': forms.RadioSelect(choices=yes_no),
            'mi_is_nursing': forms.RadioSelect(choices=yes_no),
            'mi_is_birth_control': forms.RadioSelect(choices=yes_no),
            'mi_select_disease':forms.CheckboxSelectMultiple(choices=diseases),
        }

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
            'mi_is_hospitalized_folloup': 'If yes, explain',
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
            'treatment_date',
            'tooth_number',
            'treatment_procedure',
            'treatment_dentist',
            'amount_charged',
            'amount_paid',
            'balance',
            'next_appointment'
        ]
        widgets = {
            'treatment_date': forms.DateInput(attrs={'type': 'date'}),
            'next_appointment': forms.DateInput(attrs={'type': 'date'}),
        }


















class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)


    class Meta:
        model = CustomUser
        fields = ('email','username')

    def clean(self):
        cleaned_data = super().clean()
        role = 'USER'  # Because you're registering regular users here
        username = cleaned_data.get('username')

        if role == 'USER' and not username:
            raise forms.ValidationError("Username is required for Users.")
        return cleaned_data

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'USER'  # Force default role
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user