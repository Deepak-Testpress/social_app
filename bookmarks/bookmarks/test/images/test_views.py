from django.test import TestCase
from django.urls import reverse
from images.models import Image
from .test_model_mixin import ModelMixinTestCase


class ImageCreateView(ModelMixinTestCase, TestCase):
    def test_image_create_template_used(self):

        self.client.login(username="john", password="johnpassword")
        response = self.client.get(reverse("images:create"))

        self.assertTemplateUsed(response, "images/image/create.html")

    def test_image_create_adds_new_image_to_database(self):
        self.client.login(username="john", password="johnpassword")

        self.client.post(
            reverse("images:create"),
            data={
                "title": "test-image",
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
            },
        )
        self.assertTrue(Image.objects.filter(user=self.user).exists())

    def test_image_detail_template_used(self):
        self.client.login(username="john", password="johnpassword")
        Image.objects.create(
            user=self.user,
            title="test-image",
            slug="test-imagez",
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
        )

        response = self.client.get(
            reverse("images:detail", args=[1, "test-imagez"])
        )

        self.assertTemplateUsed(response, "images/image/detail.html")

    def test_image_from_database_exists_in_detail_view(self):
        self.client.login(username="john", password="johnpassword")

        self.image = Image.objects.create(
            user=self.user,
            title="test-image",
            slug="test-image",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
        )
        response = self.client.get(
            reverse("images:detail", args=[1, "test-image"])
        )

        self.assertEqual(response.context.get("image"), self.image)

    def test_detail_view_returns_404_for_no_image(self):
        self.client.login(username="john", password="johnpassword")

        response = self.client.get(
            reverse("images:detail", args=[1, "test-image"])
        )
        self.assertEqual(response.status_code, 404)

    def test_image_like_succeeds_with_valid_image(self):
        self.client.login(username="john", password="johnpassword")

        self.image = Image.objects.create(
            user=self.user,
            title="test",
            slug="test",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
        )
        response = self.client.post(
            reverse("images:like"),
            {"id": 1, "action": "like"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )

        self.assertEqual(response.content.decode(), '{"status": "ok"}')

    def test_image_unlike_succeeds_with_valid_image(self):
        self.client.login(username="john", password="johnpassword")

        self.image = Image.objects.create(
            user=self.user,
            title="tests",
            slug="tests",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
        )

        self.client.post(
            reverse("images:like"),
            {"id": 1, "action": "like"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )

        response = self.client.post(
            reverse("images:like"),
            {"id": 1, "action": "unlike"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )

        self.assertEqual(response.content.decode(), '{"status": "ok"}')

    def test_image_like_fails_when_image_id_and_action_is_none(self):
        self.client.login(username="john", password="johnpassword")

        self.image = Image.objects.create(
            user=self.user,
            title="test",
            slug="test",
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Berlin_Opera_UdL_asv2018-05.jpg/800px-Berlin_Opera_UdL_asv2018-05.jpg",
        )
        response = self.client.post(
            reverse("images:like"),
            {"id": "None", "action": "None"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        self.assertEqual(response.content.decode(), '{"status": "error"}')

    def test_image_like_returns_400_when_directly_called_with_url(self):
        self.client.login(username="john", password="johnpassword")
        response = self.client.post(
            reverse("images:like"),
        )

        self.assertEqual(response.status_code, 400)

    def test_image_list_templates_used(self):
        self.client.login(username="john", password="johnpassword")
        self.create_images(5)
        response = self.client.get(reverse("images:list"))
        self.assertTemplateUsed(
            response, "images/image/list.html", "images/image/list_ajax.html"
        )

    def test_images_list_renders_first_page_when_page_not_an_integer(self):
        self.client.login(username="john", password="johnpassword")
        response = self.client.get(
            reverse("images:list"),
            {"images": self.create_images(30)},
        )
        self.assertEqual(response.context.get("images").number, 1)
