"""Project roles"""
from rolepermissions.roles import AbstractUserRole


class Doctor(AbstractUserRole):
    """Doctor permissions"""

    available_permissions = {
        # user
        "add_auth_user": False,
        "view_auth_user": True,
        "change_auth_user": False,
        "delete_auth_user": False,
        # clinic
        "add_auth_clinic": False,
        "view_auth_clinic": True,
        "change_auth_clinic": False,
        "delete_auth_clinic": False,
        # module
        "add_auth_module": False,
        "view_auth_module": True,
        "change_auth_module": True,
        "delete_auth_module": False,
        # pacient
        "add_auth_pacient": True,
        "view_auth_pacient": True,
        "change_auth_pacient": True,
        "delete_auth_pacient": True,
        # desk
        "add_auth_desk": True,
        "view_auth_desk": True,
        "change_auth_desk": True,
        "delete_auth_desk": True,
        # plan
        "add_auth_plan": True,
        "view_auth_plan": True,
        "change_auth_plan": True,
        "delete_auth_plan": True,
        # license
        "add_auth_license": False,
        "view_auth_license": False,
        "change_auth_license": False,
        "delete_auth_license": False,
        # schedule
        "add_auth_schedule_event": True,
        "view_auth_schedule_event": True,
        "change_auth_schedule_event": True,
        "delete_auth_schedule_event": True,
    }


class Tecnical(AbstractUserRole):
    """Tecnical permissions"""

    available_permissions = {
        # user
        "add_auth_user": False,
        "view_auth_user": True,
        "change_auth_user": False,
        "delete_auth_user": False,
        # clinic
        "add_auth_clinic": False,
        "view_auth_clinic": True,
        "change_auth_clinic": False,
        "delete_auth_clinic": False,
        # module
        "add_auth_module": False,
        "view_auth_module": True,
        "change_auth_module": False,
        "delete_auth_module": False,
        # pacient
        "add_auth_pacient": True,
        "view_auth_pacient": True,
        "change_auth_pacient": True,
        "delete_auth_pacient": True,
        # desk
        "add_auth_desk": True,
        "view_auth_desk": True,
        "change_auth_desk": True,
        "delete_auth_desk": True,
        # plan
        "add_auth_plan": True,
        "view_auth_plan": True,
        "change_auth_plan": True,
        "delete_auth_plan": True,
        # license
        "add_auth_license": False,
        "view_auth_license": True,
        "change_auth_license": False,
        "delete_auth_license": False,
        # schedule
        "add_auth_schedule_event": True,
        "view_auth_schedule_event": True,
        "change_auth_schedule_event": True,
        "delete_auth_schedule_event": True,
    }


class Assistant(AbstractUserRole):
    """Assistant permissions"""

    available_permissions = {
        # user
        "add_auth_user": False,
        "view_auth_user": True,
        "change_auth_user": True,
        "delete_auth_user": False,
        # clinic
        "add_auth_clinic": False,
        "view_auth_clinic": True,
        "change_auth_clinic": True,
        "delete_auth_clinic": False,
        # module
        "add_auth_module": False,
        "view_auth_module": True,
        "change_auth_module": True,
        "delete_auth_module": False,
        # pacient
        "add_auth_pacient": True,
        "view_auth_pacient": True,
        "change_auth_pacient": True,
        "delete_auth_pacient": True,
        # desk
        "add_auth_desk": True,
        "view_auth_desk": True,
        "change_auth_desk": True,
        "delete_auth_desk": True,
        # plan
        "add_auth_plan": True,
        "view_auth_plan": True,
        "change_auth_plan": True,
        "delete_auth_plan": True,
        # license
        "add_auth_license": False,
        "view_auth_license": True,
        "change_auth_license": False,
        "delete_auth_license": False,
        # schedule
        "add_auth_schedule_event": True,
        "view_auth_schedule_event": True,
        "change_auth_schedule_event": True,
        "delete_auth_schedule_event": True,
    }


class Manager(AbstractUserRole):
    """Manager permissions"""

    available_permissions = {
        # user
        "add_auth_user": True,
        "view_auth_user": True,
        "change_auth_user": True,
        "delete_auth_user": True,
        # clinic
        "add_auth_clinic": True,
        "view_auth_clinic": True,
        "change_auth_clinic": True,
        "delete_auth_clinic": True,
        # module
        "add_auth_module": True,
        "view_auth_module": True,
        "change_auth_module": True,
        "delete_auth_module": True,
        # pacient
        "add_auth_pacient": True,
        "view_auth_pacient": True,
        "change_auth_pacient": True,
        "delete_auth_pacient": True,
        # desk
        "add_auth_desk": True,
        "view_auth_desk": True,
        "change_auth_desk": True,
        "delete_auth_desk": True,
        # plan
        "add_auth_plan": True,
        "view_auth_plan": True,
        "change_auth_plan": True,
        "delete_auth_plan": True,
        # license
        "add_auth_license": True,
        "view_auth_license": True,
        "change_auth_license": True,
        "delete_auth_license": True,
        # schedule
        "add_auth_schedule_event": True,
        "view_auth_schedule_event": True,
        "change_auth_schedule_event": True,
        "delete_auth_schedule_event": True,
    }


class Admin(AbstractUserRole):
    """Admin permissions"""

    available_permissions = {
        # user
        "add_auth_user": True,
        "view_auth_user": True,
        "change_auth_user": True,
        "delete_auth_user": True,
        # clinic
        "add_auth_clinic": True,
        "view_auth_clinic": True,
        "change_auth_clinic": True,
        "delete_auth_clinic": True,
        # module
        "add_auth_module": True,
        "view_auth_module": True,
        "change_auth_module": True,
        "delete_auth_module": True,
        # pacient
        "add_auth_pacient": True,
        "view_auth_pacient": True,
        "change_auth_pacient": True,
        "delete_auth_pacient": True,
        # desk
        "add_auth_desk": True,
        "view_auth_desk": True,
        "change_auth_desk": True,
        "delete_auth_desk": True,
        # plan
        "add_auth_plan": True,
        "view_auth_plan": True,
        "change_auth_plan": True,
        "delete_auth_plan": True,
        # license
        "add_auth_license": True,
        "view_auth_license": True,
        "change_auth_license": True,
        "delete_auth_license": True,
        # schedule
        "add_auth_schedule_event": True,
        "view_auth_schedule_event": True,
        "change_auth_schedule_event": True,
        "delete_auth_schedule_event": True,
    }
