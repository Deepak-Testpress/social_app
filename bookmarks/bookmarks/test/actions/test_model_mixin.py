from django.test import TestCase
from images.models import Image
from actions.models import Action
from django.contrib.auth.models import User


class ModelMixinTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            username="john", password="johnpassword"
        )
        self.user_2 = User.objects.create_user(
            username="david", password="davidpassword"
        )

        self.image = Image.objects.create(
            user=self.user_2,
            title="tests",
            slug="tests",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
        )
