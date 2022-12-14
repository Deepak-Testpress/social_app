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


class ProfileEdit(ModelMixinTestCase, TestCase):
    def test_edit_profile_template_used(self):
        self.client.login(username="john", password="johnpassword")
        response = self.client.get(reverse("edit"))

        self.assertTemplateUsed(response, "account/edit.html")

    def test_editing_user_profile_succeeds(self):

        self.client.login(username="john", password="johnpassword")
        self.client.post(
            reverse("edit"),
            data={
                "first_name": "mosh",
            },
        )
        user = User.objects.get(username="john")
        self.assertEqual(user.first_name, "mosh")


class UserDetailView(ModelMixinTestCase, TestCase):
    def test_user_detail_template_used(self):

        self.client.login(username="john", password="johnpassword")
        response = self.client.get(reverse("user_detail", args=["john"]))

        self.assertTemplateUsed(response, "account/user/detail.html")

    def test_user_detail_returns_404_for_invalid_user(self):

        self.client.login(username="john", password="johnpassword")
        response = self.client.get(
            reverse("user_detail", args=["invalid-user"])
        )

        self.assertEqual(response.status_code, 404)
