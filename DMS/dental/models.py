from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

#Create a manager to help us create users
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        role = extra_fields.pop('role', 'USER')
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'ADMIN')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
# The Actual User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('DENTIST', 'Dentist'),
        ('ADMIN', 'Admin'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"
    
# ADMIN 
class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    can_add_patients = models.BooleanField(default=True)
    # more admin-specific fields if needed


# DENTIST
class DentistProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

# PATIENT
class Patient(models.Model):
    # Patient Information Record
    last_name = models.CharField(max_length=100, null=False)
    first_name = models.CharField(max_length=100, null=False)
    middle_name = models.CharField(max_length=100, null=False)
    nickname = models.CharField(max_length=100,null=True, blank=True)
    birthdate = models.DateField( null=False)
    age = models.PositiveIntegerField(default=0,null=False)
    sex_choices = [
        ('M','Male'),
        ('F','Female'),
    ]
    sex = models.CharField(max_length=10, choices=sex_choices, null=False, default=None)
    religion = models.CharField(max_length=100, null=False)
    nationality = models.CharField(max_length=100, null=False)
    home_address = models.CharField(max_length=255, null=False)
    occupation = models.CharField(max_length=100, null=False)
    dental_insurance = models.CharField(max_length=254, null=True, blank=True)
    dental_insurance_effective_date = models.DateField(null=True, blank=True)

    # For Minors
    for_minors_parent_or_guardian_name = models.CharField(max_length=255, null=False)
    for_minors_parent_or_guardian_occupation = models.CharField(max_length=100, null=False)

    # Contacts
    home_no = models.CharField(max_length=255, null=True, blank=True)
    office_no = models.CharField(max_length=255, null=True, blank=True)
    fax_no = models.CharField(max_length=255, null=True, blank=True)
    cel_mobile_no = models.IntegerField(null=False)
    email = models.CharField(max_length=100, null=False)


    # Referral Thanks
    referral_thanks = models.CharField(max_length=255, null=True, blank=True)
    dental_consultation_reason = models.CharField(max_length=255, null=True, blank=True)

    # Dental History 
    prev_dentist = models.CharField(max_length=255, null=True, blank=True)
    last_dental_visit = models.CharField(max_length=255, null=True, blank=True)

    # Medical History 
    physician_name = models.CharField(max_length=255, null=True, blank=True)
    physician_specialty = models.CharField(max_length=255, null=True, blank=True)
    office_address = models.CharField(max_length=255, null=True, blank=True)
    office_no = models.CharField(max_length=255, null=True, blank=True)
    
    # Medical Information
    yes_no = [
        ('YES','Yes'),
        ('NO','No'),
    ]
    mi_isgoodhealth = models.CharField(max_length=255, choices=yes_no, default=None, null=False)

    mi_is_under_medical_treatment = models.CharField(max_length=255, choices=yes_no, default=None, null=False)
    mi_is_under_medical_treatment_followup = models.CharField(max_length=255, null=True, blank=True)

    mi_is_serious_illness = models.CharField(max_length=255 , choices=yes_no, default=None, null=False)
    mi_is_serious_illness_followup = models.CharField(max_length=255, null=True, blank=True)

    mi_is_hospitalized = models.CharField(max_length=255, choices=yes_no, default=None, null=False)
    mi_is_hospitalized_folloup = models.CharField(max_length=255, null=True, blank=True)

    mi_is_taking_prescription = models.CharField(max_length=255, choices=yes_no, default=None, null=False)
    mi_is_taking_prescription_followup = models.CharField(max_length=255, null=True, blank=True)

    mi_is_using_tobacco = models.CharField(max_length=255, choices=yes_no, default=None, null=False)

    allergies = [
        ('LOCAL ANESTHETIC','Local Anesthetic (ex. Lidocaine)'),
        ('PENICILIN, ANTIBIOTICS','Penicilin, Antibiotics'),
        ('SULFA DRUGS','Sulfa Drugs'),
        ('ASPIRIN','Aspirin'),
        ('LATEX','Latex'),
        ('OTHERS','Others')
    ]
    mi_is_allergic = models.JSONField(default=list, choices=allergies, null=True, blank=True)
    mi_is_allergic_others = models.CharField(max_length=255, null=True, blank=True)

    mi_bleeding_time = models.CharField(max_length=255, blank=True, null=True)

    # MI For Women Only
    mi_is_pregnant = models.CharField(max_length=255, choices=yes_no, default=None, null=True,blank=True)
    mi_is_nursing = models.CharField(max_length=255, choices=yes_no, default=None, null=True, blank=True)
    mi_is_birth_control = models.CharField(max_length=255, choices=yes_no, default=None, null=True, blank=True)
    
    mi_bloodtype = models.CharField(max_length=255, null=False)
    mi_bloodpressure = models.CharField(max_length=255, null=False)

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

    mi_select_disease = models.JSONField(default=list, choices=diseases, null=True, blank=True)
    mi_select_disease_others = models.CharField(max_length=255, null=True, blank=True)






    synced_user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)  # For syncing with user login

    def __str__(self):
        return f'{self.last_name}, {self.first_name} {self.middle_name}'




# INTRAORAL EXAMINATION
class IntraoralExamination(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dentist = models.ForeignKey(DentistProfile, on_delete=models.SET_NULL, null=True)
    exam_date = models.DateField(auto_now_add=True)
    notes = models.TextField()


# TREATMENT RECORDS
class TreatmentRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment_details = models.TextField()
    date_updated = models.DateTimeField(auto_now=True)

