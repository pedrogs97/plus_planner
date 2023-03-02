"""
Class of roles permissions
"""
from rest_framework_roles.roles import is_user, is_anon, is_admin
from plus_planner.utils.constants import MANAGER, DOCTOR, ASSISTANT, NURSE


def is_manager(request, view):
    """
    Check if is manager
    """
    clinic_id = request.query_params.get("clinic", None)
    if clinic_id is None:
        return False
    return (
        is_user(request, view)
        and (MANAGER in request.user.get_roles_by_clinic(clinic_id))
        and (request.user.is_clinic)
    )


def is_doctor(request, view):
    """
    Check if is docter
    """
    clinic_id = request.query_params.get("clinic", None)
    if clinic_id is None:
        return False
    return is_user(request, view) and (
        DOCTOR in request.user.get_roles_by_clinic(clinic_id)
    )


def is_assistant(request, view):
    """
    Check if is assistant
    """
    clinic_id = request.query_params.get("clinic", None)
    if clinic_id is None:
        return False
    return is_user(request, view) and (
        ASSISTANT in request.user.get_roles_by_clinic(clinic_id)
    )


def is_nurse(request, view):
    """
    Check if is nurse
    """
    clinic_id = request.query_params.get("clinic", None)
    if clinic_id is None:
        return False
    return is_user(request, view) and (
        NURSE in request.user.get_roles_by_clinic(clinic_id)
    )


ROLES = {
    # Django out-of-the-box
    "admin": is_admin,
    "user": is_user,
    "anon": is_anon,
    # Some custom role examples
    "manager": is_manager,
    "doctor": is_doctor,
    "assistant": is_assistant,
    "nurse": is_nurse,
}
