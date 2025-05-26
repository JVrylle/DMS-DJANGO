from django.contrib import admin
from .models import CustomUser, Patient, IntraoralExamination, TreatmentRecord, AdminLog,Appointment, Notification

# Register your models here.
admin.site.register(CustomUser)
# admin.site.register(AdminProfile)
# admin.site.register(DentistProfile)
admin.site.register(Patient)
admin.site.register(IntraoralExamination)
admin.site.register(TreatmentRecord)
admin.site.register(AdminLog)
admin.site.register(Appointment)
admin.site.register(Notification)
