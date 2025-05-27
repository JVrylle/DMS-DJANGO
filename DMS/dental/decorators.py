from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied
            if request.user.role not in allowed_roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from .models import Patient

def patient_verified_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.patient_verification_status = 'verified'

        try:
            patient = Patient.objects.get(synced_user=request.user)
            if not patient.is_verified:
                request.patient_verification_status = 'unverified'
        except Patient.DoesNotExist:
            request.patient_verification_status = 'no_patient'

        return view_func(request, *args, **kwargs)
    return _wrapped_view



from functools import wraps
from django.shortcuts import render
from .models import Patient

def with_progress_bar(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        patient = Patient.objects.filter(synced_user=user).first()

        progress = {
            'account_created': user.is_authenticated,
            'pir_filled': bool(patient),
            'hir_filled': patient.is_complete if patient else False,
            'verified': patient.is_verified if patient else False,
        }

        request.progress = progress  # Save in request object

        response = view_func(request, *args, **kwargs)

        # If the view returned a rendered response, inject the progress context manually
        if hasattr(response, 'context_data'):
            response.context_data['progress'] = progress
        elif hasattr(response, 'status_code') and hasattr(response, 'content') and 'text/html' in response.get('Content-Type', ''):
            # Rendered via render() — attempt to patch context
            # This part cannot modify already-rendered HTML — use middleware if needed
            pass

        return response
    return _wrapped_view