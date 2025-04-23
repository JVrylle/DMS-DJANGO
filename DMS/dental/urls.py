from django.urls import path
from . import views 

urlpatterns = [
    # WEBSITE
    path('',views.website,name='website'),

    # USER DASHBOARD
    path('user/dashboard/',views.user_dash, name='user_dash'),
    path('user/appointments/',views.user_appointments, name='user_appointments'),
    path('user/analytics/',views.user_analytics, name='user_analytics'),
    path('user/notifications/',views.user_notifications, name='user_notifications'),
    path('user/prescription/',views.user_prescription, name='user_prescription'),
    path('user/health-record/',views.user_health_record, name='user_health_record'),
    path('user/emergency/',views.user_emergency, name='user_emergency'),
    path('user/faq/',views.user_faq, name='user_faq'),

    # DENTIST DASHBOARD
    path('Dentist/',views.dentist_dash,name='dentist_dash'),

    # ADMIN DASHBOARD
    path('Admin/',views.admin_dash,name='admin_dash'),
    

    # TESTING
    path('testing/',views.testing, name='testing'),    
]