"""
Test account module
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from plus_planner.models.account import User, Clinic, ClinicUserRole
from plus_planner.views.account import UsersView
from plus_planner.utils.constants import MANAGER, DOCTOR, ASSISTANT, NURSE


class UserTests(APITestCase):
    """
    User API test case
    """

    def setUp(self) -> None:
        super().setUp()
        self.user_test_manager = User(
            full_name="Testador",
            username="teste",
            email="teste@example.com",
            taxpayer_identification="99999999999",
            is_clinic=True,
        )
        self.user_test_assistant = User(
            full_name="Testador",
            username="teste",
            email="teste@example.com",
            taxpayer_identification="99999999999",
            is_clinic=True,
        )
        self.user_test_doctor = User(
            full_name="Testador",
            username="teste",
            email="teste@example.com",
            taxpayer_identification="99999999999",
            is_clinic=True,
        )
        self.user_test_nurse = User(
            full_name="Testador",
            username="teste",
            email="teste@example.com",
            taxpayer_identification="99999999999",
            is_clinic=True,
        )
        self.user_test_manager.set_password("123123")
        self.user_test_manager.save()
        self.clinic_test = Clinic.objects.create(
            company_name="Clinica teste",
            taxpayer_identification="9999999999999",
        )
        self.clinic_test.account.add(
            self.user_test_manager, through_defaults={"role_type": MANAGER}
        )
        self.clinic_test.account.add(
            self.user_test_doctor, through_defaults={"role_type": DOCTOR}
        )
        self.clinic_test.account.add(
            self.user_test_assistant, through_defaults={"role_type": ASSISTANT}
        )
        self.clinic_test.account.add(
            self.user_test_nurse, through_defaults={"role_type": NURSE}
        )

    def test_login(self):
        """
        Testing login view.
        """
        url = reverse("login")
        data = {"email": "teste@email.com", "password": "123123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(dict(response.data).keys(), ["access", "refresh"])

    def test_refresh_token(self):
        """
        Testing refresh token view.
        """
        pair_tokens = self.user_test_manager.get_tokens_for_user()
        url = reverse("token_refresh")
        data = {"refresh": pair_tokens["refresh"]}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(dict(response.data).keys(), ["access"])

    def test_list_user(self):
        """
        Testing refresh token view.
        """
        # TODO validar para todas as roles
        factory = APIRequestFactory()
        view = UsersView.as_view()
        pair_tokens = self.user_test_manager.get_tokens_for_user()
        url = reverse("user_view")
        request = factory.get(f"{url}?clinic={self.clinic_test.id}")
        force_authenticate(
            request, user=self.user_test_manager, token=pair_tokens["access"]
        )
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_role(self):
        """
        Testing refresh token view.
        """
        self.assertEqual(
            self.user_test_manager.get_role_by_clinic(self.clinic_test.id), MANAGER
        )
