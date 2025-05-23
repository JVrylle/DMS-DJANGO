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
    sex = models.CharField(max_length=10, null=False, choices=sex_choices)
    religion = models.CharField(max_length=100, null=False)
    nationality = models.CharField(max_length=100, null=False)
    home_address = models.CharField(max_length=255, null=False)
    occupation = models.CharField(max_length=100, null=False)
    dental_insurance = models.CharField(max_length=254, null=True, blank=True)
    dental_insurance_effective_date = models.DateField(null=True, blank=True)

    # For Minors
    for_minors_parent_or_guardian_name = models.CharField(max_length=255, null=True, blank=True)
    for_minors_parent_or_guardian_occupation = models.CharField(max_length=100, null=True, blank=True)

    # Contacts
    home_no = models.CharField(max_length=255, null=True, blank=True)
    office_no = models.CharField(max_length=255, null=True, blank=True)
    fax_no = models.CharField(max_length=255, null=True, blank=True)
    cel_mobile_no = models.CharField(max_length=20, null=False)
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
    physician_office_address = models.CharField(max_length=255, null=True, blank=True)
    physician_office_no = models.CharField(max_length=255, null=True, blank=True)

    # Medical Information
    yes_no = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    mi_isgoodhealth = models.CharField(max_length=10, null=True, blank=True, choices=yes_no)
    mi_is_under_medical_treatment = models.CharField(max_length=10, null=True, blank=True, choices=yes_no)
    mi_is_under_medical_treatment_followup = models.CharField(max_length=255, null=True, blank=True)
    mi_is_serious_illness = models.CharField(max_length=10, null=True, blank=True, choices=yes_no)
    mi_is_serious_illness_followup = models.CharField(max_length=255, null=True, blank=True)
    mi_is_hospitalized = models.CharField(max_length=10, null=True, blank=True, choices=yes_no)
    mi_is_hospitalized_followup = models.CharField(max_length=255, null=True, blank=True)
    mi_is_taking_prescription = models.CharField(max_length=10, null=True, blank=True, choices=yes_no)
    mi_is_taking_prescription_followup = models.CharField(max_length=255, null=True, blank=True)
    mi_is_using_tobacco = models.CharField(max_length=10, null=True, blank=True, choices=yes_no)
    mi_is_using_dangerous_drugs = models.CharField(max_length=10, null=True, blank=True, choices=yes_no)

    mi_is_allergic = models.JSONField(default=list, null=True, blank=True)
    mi_is_allergic_others = models.CharField(max_length=255, null=True, blank=True)
    mi_bleeding_time = models.CharField(max_length=255, null=True, blank=True)

    # MI For Women Only
    mi_is_pregnant = models.CharField(max_length=10, null=True, blank=True, choices=yes_no)
    mi_is_nursing = models.CharField(max_length=10, null=True, blank=True, choices=yes_no)
    mi_is_birth_control = models.CharField(max_length=10, null=True, blank=True, choices=yes_no)

    mi_bloodtype = models.CharField(max_length=255, null=True, blank=True)
    mi_bloodpressure = models.CharField(max_length=255, null=True, blank=True)
    mi_select_disease = models.JSONField(default=list, null=True, blank=True)
    mi_select_disease_others = models.CharField(max_length=255, null=True, blank=True)

    # Sync and Status
    synced_user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    is_complete = models.BooleanField(default=False)  # Has medical/dental data been filled?
    is_verified = models.BooleanField(default=False)  # Has admin verified the record?

    def __str__(self):
        return f'{self.last_name}, {self.first_name} {self.middle_name}'





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
    amount_charged = models.IntegerField(null=True)
    amount_paid = models.IntegerField(null=True)
    balance = models.IntegerField(null=True)
    next_appointment = models.DateField(max_length=255,null=True)

# Appointments
class Appointment(models.Model):
    PURPOSE_CHOICES = [
        ('Checkup', 'Checkup'),
        ('Cleaning', 'Cleaning'),
        ('Filling', 'Filling'),
        ('Extraction', 'Extraction'),
        ('Crown', 'Crown'),
        ('Root Canal', 'Root Canal'),
        ('Adjust', 'Adjust'),
        ('Whitening', 'Whitening'),
        ('Bonding (Braces)', 'Bonding (Braces)'),
        ('Others','Others'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('No Show', 'No Show'),
        ('Pending-Walk-in', 'Pending-Walk-in'),
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

    # New fields
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

    def __str__(self):
        return f"Notification for {self.user.email}"


# PRESCRIPTIONS
class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    medication = models.TextField()
    dosage = models.TextField()
    instructions = models.TextField()
    issued_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient} on {self.issued_date}"



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
