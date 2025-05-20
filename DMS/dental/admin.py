from django.contrib import admin
from .models import CustomUser, Patient, IntraoralExamination, TreatmentRecord, AdminLog

# Register your models here.
admin.site.register(CustomUser)
# admin.site.register(AdminProfile)
# admin.site.register(DentistProfile)
admin.site.register(Patient)
admin.site.register(IntraoralExamination)
admin.site.register(TreatmentRecord)
admin.site.register(AdminLog)

