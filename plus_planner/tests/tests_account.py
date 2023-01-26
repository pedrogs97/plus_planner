"""
Test account module
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from plus_planner.models.account import User


class UserTests(APITestCase):
    """
    User API test case
    """

    def setUp(self) -> None:
        super().setUp()
        self.user_test = User(
            full_name="Testador",
            username="teste",
            email="teste@email.com",
            taxpayer_identification="99999999999",
        )
        self.user_test.set_password("123123")
        self.user_test.save()

    def test_login(self):
        """
        Testing login view.
        """
        url = reverse("login")
        data = {"email": "teste@email.com", "password": "123123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        """
        Testing refresh token view.
        """
        url = reverse("login")
        data = {"email": "teste@email.com", "password": "123123"}
        response = self.client.post(url, data, format="json")

        url = reverse("token_refresh")
        data = {"refresh": response.json()["refresh"]}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
