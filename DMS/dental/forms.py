from django import forms
from .models import Patient

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
                  'office_address',
                  'office_no',
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
                  'mi_is_allergic',
                  'mi_is_allergic_others',
                  'mi_bleeding_time',
                  'mi_is_pregnant',
                  'mi_is_nursing',
                  'mi_is_birth_control',
                  'mi_bloodtype',
                  'mi_bloodpressure',
                  'email',

                  ]

        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'dental_insurance_effective_date': forms.DateInput(attrs={'type': 'date'}),
            'sex': forms.RadioSelect(),
            'mi_isgoodhealth': forms.RadioSelect(),
            'mi_is_under_medical_treatment': forms.RadioSelect(),
            'mi_is_serious_illness': forms.RadioSelect(),   
            'mi_is_hospitalized': forms.RadioSelect(),
            'mi_is_taking_prescription': forms.RadioSelect(),
            'mi_is_using_tobacco': forms.RadioSelect(),
            'mi_is_allergic': forms.CheckboxSelectMultiple(),
            'mi_is_pregnant': forms.RadioSelect(),
            'mi_is_nursing': forms.RadioSelect(),
            'mi_is_birth_control': forms.RadioSelect(),
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
            'for_minors_parent_or_guardian_name': 'Parent/Guardian Name',
            'for_minors_parent_or_guardian_occupation': 'Parent/Guardian Occupation',
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
            'office_address': 'Physician Office Address',
            'mi_isgoodhealth': 'Are you in good health?',
            'mi_is_under_medical_treatment': 'Under medical treatment?',
            'mi_is_under_medical_treatment_followup': 'If yes, explain',
            'mi_is_serious_illness': 'Any serious illness?',
            'mi_is_serious_illness_followup': 'If yes, explain',
            'mi_is_hospitalized': 'Have you been hospitalized?',
            'mi_is_hospitalized_folloup': 'If yes, explain',
            'mi_is_taking_prescription': 'Taking any prescriptions?',
            'mi_is_taking_prescription_followup': 'If yes, explain',
            'mi_is_using_tobacco': 'Do you use tobacco?',
            'mi_is_allergic': 'Allergies (Check all that apply)',
            'mi_is_allergic_others': 'Other allergies (if any)',
            'mi_bleeding_time': 'Bleeding Time',
            'mi_is_pregnant': 'Are you pregnant?',
            'mi_is_nursing': 'Are you nursing?',
            'mi_is_birth_control': 'Using birth control?',
            'mi_bloodtype': 'Blood Type',
            'mi_bloodpressure': 'Blood Pressure',
        }

        #  Apply the custom labels
        for field_name, label in custom_labels.items():
            if field_name in self.fields:
                self.fields[field_name].label = label


class ConsentForm(forms.Form):
    consent_signed = forms.BooleanField(label="Patient has signed digital informed consent.")
