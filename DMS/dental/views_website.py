from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .decorators import role_required
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login


# WEBSITE
def website(request):
    register_form = CustomUserCreationForm()
    login_form = AuthenticationForm()

    return render(request, 'Website/website.html', {
        'register_form': register_form,
        'login_form': login_form,
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Auto login after registration


            return redirect_user_by_role(user)
        else:
            login_form = AuthenticationForm()
            return render(request, 'Website/website.html', {
                'register_form': form,
                'login_form': login_form,
                'show_register': True  # Optional: used to open modal via JS
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
    return redirect('user_dash')

