from django.test import TestCase
from actions.models import Action
from .test_model_mixin import ModelMixinTestCase
from django.urls import reverse


class ActionStream(ModelMixinTestCase, TestCase):
    def test_action_stream_shows_to_others_in_dashboard(self):
        self.client.login(username="john", password="johnpassword")
        self.client.post(
            reverse("images:like"),
            {"id": 1, "action": "like"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )

        self.client.login(username="david", password="davidpassword")
        dashboard_display = self.client.get(reverse("dashboard"))

        self.assertQuerysetEqual(
            dashboard_display.context.get("actions"),
            Action.objects.filter(verb="likes"),
        )

    def test_action_stream_does_not_show_our_own_action_in_dashboard(self):
        self.client.login(username="john", password="johnpassword")
        self.client.post(
            reverse("images:like"),
            {"id": 1, "action": "like"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        dashboard_display = self.client.get(reverse("dashboard"))

        self.assertQuerysetEqual(dashboard_display.context.get("actions"), [])
