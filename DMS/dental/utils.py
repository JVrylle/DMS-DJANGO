from .models import AdminLog

def log_admin_action(
    log_type,
    description,
    model=None,
    obj_id=None,
    metadata=None,
    admin=None
):
    AdminLog.objects.create(
        log_type=log_type,
        action_description=description,
        affected_model=model,
        affected_object_id=obj_id,
        metadata=metadata,
        admin=admin
    )


# USE THIS INSIDE VIEWS.py or SIGNALS

# from .utils import log_admin_action

# # Logging a new patient registration (SYSTEM)
# log_admin_action(
#     log_type='SYSTEM',
#     description=f"New user submitted registration: {user.email}",
#     model='CustomUser',
#     obj_id=user.id
# )

# # Logging a new appointment (EVENT)
# log_admin_action(
#     log_type='EVENT',
#     description=f"Appointment booked by {user.email} with Dr. Lee",
#     model='Appointment',
#     obj_id=appointment.id,
#     metadata={"date": "2025-06-01", "time": "10:00 AM"}
# )

# # Logging an emergency (EMERGENCY)
# log_admin_action(
#     log_type='EMERGENCY',
#     description=f"Emergency reported by {user.email}",
#     model='EmergencyReport',
#     obj_id=emergency.id
# )

# # Example security log (SECURITY)
# log_admin_action(
#     log_type='SECURITY',
#     description="Repeated failed login attempts for user john_doe",
#     metadata={"ip": "192.168.0.1", "attempts": 5}
# )