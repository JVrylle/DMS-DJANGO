from django.urls import path
from . import views 

urlpatterns = [
    path('',views.website,name='website'),
    path('testing/',views.testing, name='testing'),
    path('UserDashboard/',views.user_dash,name='user_dash'),
    path('DentistDashboard/',views.dentist_dash,name='dentist_dash'),
    path('AdminDashboard/',views.admin_dash,name='admin_dash'),
    
]