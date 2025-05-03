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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    synced_user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)  # For syncing with user login

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

