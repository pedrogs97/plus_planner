"""
Class of roles permissions
"""
from rest_framework_roles.roles import is_user, is_anon, is_admin
from plus_planner.models.account import ClinicUserRole
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
        and (request.user.get_role_by_clinic(clinic_id) == MANAGER)
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
        request.user.get_role_by_clinic(clinic_id) == DOCTOR
    )


def is_assistant(request, view):
    """
    Check if is assistant
    """
    clinic_id = request.query_params.get("clinic", None)
    if clinic_id is None:
        return False
    return is_user(request, view) and (
        request.user.get_role_by_clinic(clinic_id) == ASSISTANT
    )


def is_nurse(request, view):
    """
    Check if is nurse
    """
    clinic_id = request.query_params.get("clinic", None)
    if clinic_id is None:
        return False
    return is_user(request, view) and (
        request.user.get_role_by_clinic(clinic_id) == NURSE
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
