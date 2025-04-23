from django.db import models

class Patient(models.Model):
    patient_id = models.CharField(max_length=255)
    patient_firstname = models.CharField(max_length=255)
    patient_lastname = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.patient_id} {self.patient_lastname}, {self.patient_firstname}"