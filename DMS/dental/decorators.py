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