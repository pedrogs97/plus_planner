"""
Test account module
"""
from datetime import datetime
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from plus_planner.models.account import User, Clinic, ClinicUserRole
from plus_planner.models.schedule import ScheduleEvent
from plus_planner.models.clinical import Pacient, Desk
from plus_planner.views.account import UsersView
from plus_planner.utils.constants import (
    MANAGER,
    DOCTOR,
    ASSISTANT,
    NURSE,
    ROLES,
    ADMINISTRATIVE_ROLES,
    NORMAL_ROLES,
)


class ScheduleEventsTests(APITestCase):
    """
    ScheduleEvents API test case
    """

    @classmethod
    def setUpTestData(cls) -> None:
        with open("plus_planner/tests/mock/data.json", encoding="UTF8") as data:
            cls.json_data = json.load(data)
            users_test = cls.json_data["users_test"]
            clinics_test = cls.json_data["clinics_test"]
            pacients_test = cls.json_data["pacients_test"]
            desks_test = cls.json_data["desks_test"]
            cls.users = []
            cls.clinics = []
            cls.pacients = []
            cls.desks = []
            for user_test in users_test:
                user = User(**user_test)
                user.set_password(user_test["password"])
                user.save()
                cls.users.append(user)

            for clinic_test in clinics_test:
                clinic = Clinic.objects.create(
                    company_name=clinic_test["company_name"],
                    taxpayer_identification=clinic_test["taxpayer_identification"],
                )

                for desk_test in desks_test:
                    desk = Desk.objects.create(**desk_test, clinic=clinic)
                    cls.desks.append(desk)

                for user_clinic in clinic_test["users"]:
                    clinic.account.add(
                        User.objects.get(username=user_clinic["username"]),
                        through_defaults={"role_type": user_clinic["role"]},
                    )
                cls.clinics.append(clinic)

            for pacient_test in pacients_test:
                pacient = Pacient.objects.create(**pacient_test)
                cls.pacients.append(pacient)

        all_users_clinic = User.objects.filter(clinicuserrole__clinic=cls.clinics[0])
        for user in all_users_clinic:
            cls.schedule = ScheduleEvent.objects.create(
                date=datetime.today(),
                clinic=cls.clinics[0],
                account=user,
                pacient=cls.pacients[0],
                desk=cls.desks[0],
            )

    def test_list_schedule(self):
        """
        Testing list schedule given a correct clinc.
        """
        factory = APIRequestFactory()
        view = UsersView.as_view()

        for clinic in self.clinics:
            for role in ADMINISTRATIVE_ROLES:
                clinic_user_role_query = ClinicUserRole.objects.filter(
                    clinic_id=clinic.id, role_type=role
                )
                for administrative_clinic_user_role in clinic_user_role_query:
                    pair_tokens = (
                        administrative_clinic_user_role.user.get_tokens_for_user()
                    )
                    url = reverse("user_view")
                    request = factory.get(f"{url}?clinic={clinic.id}")
                    force_authenticate(
                        request,
                        user=administrative_clinic_user_role.user,
                        token=pair_tokens["access"],
                    )
                    response = view(request)
                    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_list_user_invalid(self):
    #     """
    #     Testing list scheduel given a incorret clinc.
    #     """
    #     factory = APIRequestFactory()
    #     view = UsersView.as_view()
    #     for clinic in self.clinics:
    #         for role in NORMAL_ROLES:
    #             clinic_user_role_query = ClinicUserRole.objects.filter(
    #                 clinic_id=clinic.id, role_type=role
    #             )
    #             for administrative_clinic_user_role in clinic_user_role_query:
    #                 pair_tokens = (
    #                     administrative_clinic_user_role.user.get_tokens_for_user()
    #                 )
    #                 url = reverse("user_view")
    #                 request = factory.get(f"{url}?clinic={clinic.id}")
    #                 force_authenticate(
    #                     request,
    #                     user=administrative_clinic_user_role.user,
    #                     token=pair_tokens["access"],
    #                 )
    #                 response = view(request)
    #                 self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_get_schedule(self):
    #     """
    #     Testing get schedule
    #     """
    #     for user in self.users:
    #         for all_roles in user.get_all_roles():
    #             self.assertIn(all_roles["role_type"], ROLES)

    # def test_create_schedule(self):
    #     """
    #     Testing create schedule
    #     """
    #     for user in self.users:
    #         for clinc in user.get_clinics():
    #             self.assertIn(clinc, self.clinics)

    # def test_delete_schedule(self):
    #     """
    #     Testing delete schedule
    #     """
    #     for user in self.users:
    #         for clinc in user.get_clinics():
    #             self.assertIn(clinc, self.clinics)

    # def test_update_schedule(self):
    #     """
    #     Testing update schedule
    #     """
    #     for user in self.users:
    #         for clinc in user.get_clinics():
    #             self.assertIn(clinc, self.clinics)
