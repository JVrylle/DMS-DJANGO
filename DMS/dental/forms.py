from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'middle_name', 'last_name','birth_date','age','religion','nationality','home_address','occupation','dental_insurance','dental_insurance_effective_date','sex']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'dental_insurance_effective_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ConsentForm(forms.Form):
    consent_signed = forms.BooleanField(label="Patient has signed digital informed consent.")
