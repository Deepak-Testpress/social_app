from django.test import TestCase, Client
from .test_model_mixin import ModelMixinTestCase
from django.urls import reverse
from account.forms import UserRegistrationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class UserLogin(ModelMixinTestCase, TestCase):
    def test_account_dashboard_template_used(self):
        self.client = Client()
        self.assertTrue(self.user.is_active)
        self.client.login(username="john", password="johnpassword")
        response = self.client.get(reverse("dashboard"))

        self.assertTemplateUsed(response, "account/dashboard.html")


class UserRegister(ModelMixinTestCase, TestCase):
    def test_register_returns_user_registration_form(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(
            type(response.context.get("form")), UserRegistrationForm
        )

    def test_registeration_templates_used(self):
        response = self.client.get(reverse("register"))

        self.assertTemplateUsed(
            response, "account/register.html", "account/register_done.html"
        )

    def test_registeration_succeeds_with_valid_user_credentials(self):
        self.client.post(
            reverse("register"),
            data={
                "username": "johndoe",
                "first_name": "John",
                "email": "johndoe8@example.com",
                "password": "johnpassword",
                "password2": "johnpassword",
            },
        )
        self.assertTrue(User.objects.filter(username="john").exists())
