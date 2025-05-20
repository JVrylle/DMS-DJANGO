from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login

# FOR EMAIL VERIFICATION
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from .utils import email_verification_token

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login

from .models import CustomUser


# WEBSITE
def website(request):
    register_form = CustomUserCreationForm()
    login_form = AuthenticationForm()

    return render(request, 'Website/website.html', {
        'register_form': register_form,
        'login_form': login_form,
    })


# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request, user)  # Auto login after registration


#             return redirect_user_by_role(user)
#         else:
#             login_form = AuthenticationForm()
#             return render(request, 'Website/website.html', {
#                 'register_form': form,
#                 'login_form': login_form,
#                 'show_register': True  # Optional: used to open modal via JS
#             })
#     return redirect('website')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Don't activate until email verified
            user.save()

            # Email verification link generation
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = email_verification_token.make_token(user)
            verification_url = f"http://{current_site.domain}/activate/{uid}/{token}/"

            # Show the verification template directly in browser
            return render(request, 'email/verify_email.html', {
                'user': user,
                'verification_url': verification_url,
            })

        else:
            # Form is invalid — show errors
            login_form = AuthenticationForm()
            return render(request, 'Website/website.html', {
                'register_form': form,
                'login_form': login_form,
                'show_register': True
            })

    return redirect('website')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, form.get_user())
            return redirect_user_by_role(user)
        else:
            register_form = CustomUserCreationForm()
            return render(request, 'Website/website.html', {
                'login_form': form,
                'register_form': register_form,
                'show_login': True  # Optional: used to open modal via JS
            })
    return redirect('website')


def redirect_user_by_role(user):
    if user.role == 'ADMIN':
        return redirect('admin_dash')
    elif user.role == 'DENTIST':
        return redirect('dentist_dash')
    return redirect('user_health_record')

# FOR EMAIL VERIFICATION

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and email_verification_token.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        auth_login(request, user)
        return redirect_user_by_role(user)
    else:
        return render(request, 'Website/email_verification_failed.html')
