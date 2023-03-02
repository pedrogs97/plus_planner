"""
Test account module
"""
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from plus_planner.models.account import User, Clinic, ClinicUserRole
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


class UserTests(APITestCase):
    """
    User API test case
    """

    @classmethod
    def setUpTestData(cls) -> None:
        with open("plus_planner/tests/mock/data.json", encoding="UTF8") as data:
            cls.json_data = json.load(data)
            users_test = cls.json_data["users_test"]
            clinics_test = cls.json_data["clinics_test"]
            cls.users = []
            cls.clinics = []
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
                for user_clinic in clinic_test["users"]:
                    clinic.account.add(
                        User.objects.get(username=user_clinic["username"]),
                        through_defaults={"role_type": user_clinic["role"]},
                    )
                cls.clinics.append(clinic)

    def test_login(self):
        """
        Testing login view.
        """
        url = reverse("login")
        for user in self.json_data["users_test"]:
            data = {"email": user["email"], "password": user["password"]}
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(dict(response.data).keys(), ["access", "refresh"])

    def test_refresh_token(self):
        """
        Testing refresh token view.
        """
        for user in self.users:
            pair_tokens = user.get_tokens_for_user()
            url = reverse("token_refresh")
            data = {"refresh": pair_tokens["refresh"]}
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(dict(response.data).keys(), ["access"])

    def test_list_user(self):
        """
        Testing list users given a clinc with correct role.
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

    def test_list_user_invalid(self):
        """
        Testing list users given a clinc with incorret role.
        """
        factory = APIRequestFactory()
        view = UsersView.as_view()
        for clinic in self.clinics:
            for role in NORMAL_ROLES:
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
                    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_role(self):
        """
        Testing get user role. Test for all roles
        """
        for user in self.users:
            for all_roles in user.get_all_roles():
                self.assertIn(all_roles["role_type"], ROLES)

    def test_get_user_clinic(self):
        """
        Testing get user clinic. Test for all clinic
        """
        for user in self.users:
            for clinc in user.get_clinics():
                self.assertIn(clinc, self.clinics)
