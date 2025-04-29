from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required


# WEBSITE
def website(request):
    return render(request, 'website.html')

# USER
@role_required(['USER'])
def user_dash(request):
    return render(request, 'User/user_dash.html')

# def user_landing(request):
#     return render(request, 'User/user_landing.html')

@role_required(['USER'])
def user_appointments(request):
    return render(request, 'User/user_appointments.html')

@role_required(['USER'])
def user_analytics(request):
    return render(request, 'User/user_analytics.html')

@role_required(['USER'])
def user_notifications(request):
    return render(request, 'User/user_notifications.html')

@role_required(['USER'])
def user_prescription(request):
    return render(request, 'User/user_prescription.html')

@role_required(['USER'])
def user_health_record(request):
    return render(request, 'User/user_health_record.html')

@role_required(['USER'])
def user_emergency(request):
    return render(request, 'User/user_emergency.html')

@role_required(['USER'])
def user_faq(request):
    return render(request, 'User/user_faq.html')




# DENTIST
@role_required(['DENTIST','ADMIN'])
def dentist_dash(request):
    return render(request, 'Dentist/dentist_dash.html')

# ADMIN
@role_required(['DENTIST','ADMIN'])
def admin_dash(request):
    return render(request, 'Admin/admin_dash.html')




# TESTING
@role_required(['DENTIST','ADMIN'])
def testing(request):
    testing_list = [1,2,3,4,5]

    context = {
        'testing_list': testing_list
    }

    return render(request, 'testing.html', context)


# THIS IS TESTING 

@role_required(['ADMIN'])
def phase1_input_view(request):
    # Admin or assistant can input patient info
    pass

@role_required(['DENTIST'])
def intraoral_exam_view(request):
    # Dentist only
    pass

@role_required(['USER'])
def appointment_crud_view(request):
    # Users manage their appointments
    pass

def dashboard_redirect_view(request):
    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif request.user.role == 'DENTIST':
        return redirect('dentist_dashboard')
    else:
        return redirect('user_dashboard')
