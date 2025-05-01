from django.urls import path
from . import views 

urlpatterns = [
    # WEBSITE
    path('',views.website,name='website'),

    # USER DASHBOARD
    path('User/',views.user_dash, name='user_dash'),
    path('User/appointments/',views.user_appointments, name='user_appointments'),
    path('User/analytics/',views.user_analytics, name='user_analytics'),
    path('User/notifications/',views.user_notifications, name='user_notifications'),
    path('User/prescription/',views.user_prescription, name='user_prescription'),
    path('User/health-record/',views.user_health_record, name='user_health_record'),
    path('User/emergency/',views.user_emergency, name='user_emergency'),
    path('User/faq/',views.user_faq, name='user_faq'),

    # DENTIST DASHBOARD
    path('Dentist/',views.dentist_dash,name='dentist_dash'),
    path('Dentist/appointments/',views.dentist_appointments,name='dentist_appointments'),
    path('Dentist/patient-information-record/',views.dentist_patient_info_record,name='dentist_patient_info_record'),
    path('Dentist/health-records/',views.dentist_patient_health_records,name='dentist_patient_health_records'),
    path('Dentist/analytics/',views.dentist_analytics,name='dentist_analytics'),
    path('Dentist/notification/',views.dentist_notifications,name='dentist_notifications'),
    path('Dentist/give-prescription/',views.dentist_give_prescription,name='dentist_give_prescription'),
    path('Dentist/emergency-notifications/',views.dentist_emergency,name='dentist_emergency'),
    path('Dentist/faq/',views.dentist_faq,name='dentist_faq'),

    # ADMIN DASHBOARD
    path('Admin/',views.admin_dash,name='admin_dash'),
    path('Admin/appointments/',views.admin_appointments,name='admin_appointments'),
    path('Admin/patient-information-record/',views.admin_patient_info_records,name='admin_patient_info_records'),
    path('Admin/analytics/',views.admin_analytics,name='admin_analytics'),
    path('Admin/system-logs/',views.admin_system_logs,name='admin_system_logs'),
    path('Admin/security-logs/',views.admin_security_logs,name='admin_security_logs'),
    path('Admin/event-logs/',views.admin_event_logs,name='admin_event_logs'),
    path('Admin/emergency-logs/',views.admin_emergency_logs,name='admin_emergency_logs'),
    

    # TESTING
    path('testing/',views.testing, name='testing'),    
]