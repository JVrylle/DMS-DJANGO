from django.urls import path
from . import views, views_website, views_user, views_dentist, views_admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    # WEBSITE
    path('',views_website.website,name='website'),
    path('register/',views_website.register,name='register'),
    path('login/',views_website.login,name='login'),

    # EMAIL VERIFICATION
    path('activate/<uidb64>/<token>/', views_website.activate, name='activate'),

    # USER DASHBOARD
    path('User/',views_user.user_dash, name='user_dash'),
    path('User/appointments/',views_user.user_appointments, name='user_appointments'),
    path('User/analytics/',views_user.user_analytics, name='user_analytics'),
    path('User/notifications/',views_user.user_notifications, name='user_notifications'),
    path('User/prescription/',views_user.user_prescription, name='user_prescription'),
    path('User/health-record/',views_user.user_health_record, name='user_health_record'),
    path('User/emergency/',views_user.user_emergency, name='user_emergency'),
    path('User/faq/',views_user.user_faq, name='user_faq'),

    # DENTIST DASHBOARD
    path('Dentist/',views_dentist.dentist_dash,name='dentist_dash'),
    path('Dentist/appointments/',views_dentist.dentist_appointments,name='dentist_appointments'),
    path('Dentist/patient-information-record/',views_dentist.dentist_patient_info_record,name='dentist_patient_info_record'),
    path('Dentist/health-records/',views_dentist.dentist_patient_health_records,name='dentist_patient_health_records'),
    path('Dentist/analytics/',views_dentist.dentist_analytics,name='dentist_analytics'),
    path('Dentist/notification/',views_dentist.dentist_notifications,name='dentist_notifications'),
    path('Dentist/give-prescription/',views_dentist.dentist_give_prescription,name='dentist_give_prescription'),
    path('Dentist/emergency-notifications/',views_dentist.dentist_emergency,name='dentist_emergency'),
    path('Dentist/faq/',views_dentist.dentist_faq,name='dentist_faq'),

    # ADMIN DASHBOARD
    path('Admin/',views_admin.admin_dash,name='admin_dash'),
    path('Admin/appointments/',views_admin.admin_appointments,name='admin_appointments'),
    path('Admin/patient-information-record/',views_admin.admin_patient_info_records,name='admin_patient_info_records'),
    path('Admin/analytics/',views_admin.admin_analytics,name='admin_analytics'),
    path('Admin/system-logs/',views_admin.admin_system_logs,name='admin_system_logs'),
    path('Admin/security-logs/',views_admin.admin_security_logs,name='admin_security_logs'),
    path('Admin/event-logs/',views_admin.admin_event_logs,name='admin_event_logs'),
    path('Admin/emergency-logs/',views_admin.admin_emergency_logs,name='admin_emergency_logs'),
    

    # TESTING   
    path('testing/',views.testing, name='testing'),    
    path('forbidden/',views.forbidden, name='forbidden'),
    path('logout/', auth_views.LogoutView.as_view(next_page='website'), name='logout'),
]