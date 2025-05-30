from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth import get_user_model
from django.conf import settings



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
    username = models.CharField(max_length=150, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"
    
# PATIENT
class Patient(models.Model):
    # Patient Information Record
    last_name = models.CharField(max_length=100, null=False)
    first_name = models.CharField(max_length=100, null=False)
    middle_name = models.CharField(max_length=100, null=False)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    birthdate = models.DateField(null=False)
    age = models.PositiveIntegerField(default=0, null=False)
    
    sex_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    sex = models.CharField(max_length=10, null=False)
    religion = models.CharField(max_length=100, null=False)
    nationality = models.CharField(max_length=100, null=False)
    home_address = models.CharField(max_length=255, null=False)
    occupation = models.CharField(max_length=100, null=False)
    philhealth_no = models.CharField(max_length=20,null=True,blank=True)
    dental_insurance = models.CharField(max_length=254, null=True, blank=True)
    dental_insurance_effective_date = models.DateField(null=True, blank=True)

    # For Minors
    for_minors_parent_or_guardian_name = models.CharField(max_length=255, null=True, blank=True)
    for_minors_parent_or_guardian_occupation = models.CharField(max_length=100, null=True, blank=True)

    # Contacts
    home_no = models.CharField( max_length=20,null=True, blank=True)
    office_no = models.CharField( max_length=20,null=True, blank=True)
    fax_no = models.CharField( max_length=20,null=True, blank=True)
    cel_mobile_no = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=100, null=False)

    # Referral Thanks
    referral_thanks = models.CharField(max_length=255, null=True, blank=True)
    dental_consultation_reason = models.CharField(max_length=255, null=True, blank=True)

    # Dental History 
    prev_dentist = models.CharField(max_length=100, null=True, blank=True)
    last_dental_visit = models.DateField( null=True, blank=True)

    # Medical History 
    physician_name = models.CharField(max_length=255, null=True, blank=True)
    physician_specialty = models.CharField(max_length=100, null=True, blank=True)
    physician_office_address = models.CharField(max_length=255, null=True, blank=True)
    physician_office_no = models.CharField(max_length=100, null=True, blank=True)

    # Medical Information
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


    mi_isgoodhealth = models.CharField(max_length=10, null=True, blank=True)

    mi_is_under_medical_treatment = models.CharField(max_length=10, null=True, blank=True)
    mi_is_under_medical_treatment_followup = models.CharField(max_length=255, null=True, blank=True)

    mi_is_serious_illness = models.CharField(max_length=10, null=True, blank=True)
    mi_is_serious_illness_followup = models.CharField(max_length=255, null=True, blank=True)

    mi_is_hospitalized = models.CharField(max_length=10, null=True, blank=True, )
    mi_is_hospitalized_followup = models.CharField(max_length=255, null=True, blank=True)

    mi_is_taking_prescription = models.CharField(max_length=10, null=True, blank=True, )
    mi_is_taking_prescription_followup = models.CharField(max_length=255, null=True, blank=True)

    mi_is_using_tobacco = models.CharField(max_length=10, null=True, blank=True, )

    mi_is_using_dangerous_drugs = models.CharField(max_length=10, null=True, blank=True, )

    mi_is_allergic = models.JSONField(default=list, null=True, blank=True)
    mi_is_allergic_others = models.CharField(max_length=255, null=True, blank=True)
    mi_bleeding_time = models.CharField(max_length=255, null=True, blank=True)

    # MI For Women Only
    mi_is_pregnant = models.CharField(max_length=10, null=True, blank=True, )
    mi_is_nursing = models.CharField(max_length=10, null=True, blank=True, )
    mi_is_birth_control = models.CharField(max_length=10, null=True, blank=True, )

    mi_bloodtype = models.CharField(max_length=255, null=True, blank=True)
    mi_bloodpressure = models.CharField(max_length=255, null=True, blank=True)
    mi_select_disease = models.JSONField(default=list, null=True, blank=True)
    mi_select_disease_others = models.CharField(max_length=255, null=True, blank=True)

    # Sync and Status
    synced_user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    is_complete = models.BooleanField(default=False)  # Has medical/dental data been filled?
    is_verified = models.BooleanField(default=False)  # Has admin verified the record?
    claimed_existing_patient = models.BooleanField(null=True, blank=True)  # True = claims existing, False = claims new
    has_answered_existing_patient = models.BooleanField(default=False)  # They have answered the modal question

    # IMAGE RELATED CREDS FOR PATIENT
    digital_xrays = models.ImageField(upload_to='xrays/', blank=True, null=True)
    patient_pictures = models.ImageField(upload_to='pictures/', blank=True, null=True)
    patient_signatures = models.ImageField(upload_to='signatures/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.last_name}, {self.first_name} {self.middle_name}'
    
    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"



# INTRAORAL EXAMINATION
class IntraoralExamination(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    teeth = models.JSONField(default=list, null=True, blank=True)
    
#  THIS IS A JSON FIELD
# [
#   {"tooth": "11", "color": ["white"], "status1": "legend1", "status2": "legend2"},
#   {"tooth": "12", "color": ["red"], "status1": "legend3", "status2": "legend4"},
#   {"tooth": "13", "color": ["blue"], "status1": "legend5", "status2": "legend6"}
# ]


    xray_taken = models.JSONField(default=list, null=True, blank=True)
    xray_periapical = models.CharField(max_length=255, null=True, blank=True)
    xray_taken_others = models.CharField(max_length=255, null=True, blank=True)
    periodontal_screening = models.JSONField(default=list, null=True,blank=True)
    occlusion = models.JSONField(default=list, null=True,blank=True)
    appliances = models.JSONField(default=list, null=True,blank=True)
    appliances_others = models.CharField(max_length=255, null=True, blank=True)

    tmd = models.JSONField(default=list, null=True,blank=True)

    def __str__(self):
        return f"Intraoral Examination for {self.patient}"


# TREATMENT RECORDS
class TreatmentRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='treatment_records')

    treatment_date = models.DateField(auto_now_add=True, null=True)
    tooth_number = models.IntegerField(null=True)
    treatment_procedure = models.TextField(null=True)
    treatment_dentist = models.CharField(max_length=255,null=True)
    amount_charged = models.DecimalField(decimal_places=2, max_digits=10,null=True)
    amount_paid = models.DecimalField(decimal_places=2, max_digits=10,null=True)
    balance = models.IntegerField(null=True)
    next_appointment = models.DateField(max_length=255,null=True)

# Appointments
class Appointment(models.Model):
    PURPOSE_CHOICES = [
        ('Oral Exam', 'Oral Exam'),
        ('Oral Propelaxis', 'Oral Propelaxis'),
        ('Tooth Restoration', 'Tooth Restoration'),
        ('Tooth Extraction', 'Tooth Extraction'),
        ('Orthodontic Treatment', 'Orthodontic Treatment'),
        ('Minor Surgical Treatment', 'Minor Surgical Treatment'),
        ('Fluoride Application', 'Fluoride Application'),
        ('Prosthodontic Treatment','Prosthodontic Treatment'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('No Show', 'No Show'),
]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments',
        db_index=True
    )
    date = models.DateField(db_index=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Scheduled',
        db_index=True
    )
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES, )
    address = models.CharField(max_length=255, null=True, blank=True)

    is_first_time_visit = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_appointments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Appointments"
        ordering = ['-date',]

    def __str__(self):
        return f"{self.patient} appointment on {self.date}"


# NOTIFICATIONS
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    NOTIFICATION_TYPES = [
        ('Account', 'Account'),
        ('Appointment', 'Appointment'),
        ('Reminder', 'Reminder'),
        ('Prescription','Prescription'),
        ('Smart Suggestions','Smart Suggestions'),
        ('Emergency','Emergency'),
    ]

    redirect_url = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='Account')

    def __str__(self):
        return f"Notification for {self.user.email}"


# PRESCRIPTIONS
class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    medication = models.TextField()
    dosage = models.TextField()
    instructions = models.TextField()
    issued_date = models.DateField(auto_now_add=True)
    attachment = models.FileField(upload_to='prescriptions/', blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Rx for {self.patient.get_full_name()} - {self.medication[:20]}..."



# ADMINLOGS
User = get_user_model()

class AdminLog(models.Model):
    LOG_TYPE_CHOICES = [
        ('SYSTEM', 'System'),
        ('SECURITY', 'Security'),
        ('EVENT', 'Event'),
        ('EMERGENCY', 'Emergency'),
    ]

    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_logs')
    log_type = models.CharField(max_length=10, choices=LOG_TYPE_CHOICES)
    action_description = models.TextField()
    affected_model = models.CharField(max_length=100, null=True, blank=True)
    affected_object_id = models.PositiveIntegerField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.log_type}] at {self.timestamp} — {self.action_description[:50]}"


# Emergency Alerts
class EmergencyAlert(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='emergency_alerts')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Emergency for {self.patient} at {self.created_at}"
