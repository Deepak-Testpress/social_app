from django.test import TestCase
from django.urls import resolve, reverse
from account.views import user_login
from .test_model_mixin import ModelMixinTestCase


class TestUrls(ModelMixinTestCase, TestCase):
    def test_account_login_url(self):
        self.assertEquals(
            resolve(reverse("account:login")).func,
            user_login,
        )
