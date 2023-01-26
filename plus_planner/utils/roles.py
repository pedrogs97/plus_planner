from rest_framework_roles.roles import is_user, is_anon, is_admin

# TODO a permissão precisa ser:
# 1. Pertencer a clinica
# 2. Possuir a role necessária
def is_manager(request, view):
    return is_user(request, view) and request.user.usertype == "manager"


def is_doctor(request, view):
    return is_user(request, view) and request.user.usertype == "doctor"


def is_assistant(request, view):
    return is_user(request, view) and request.user.usertype == "assistant"


def is_nurse(request, view):
    return is_user(request, view) and request.user.usertype == "nurse"


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
