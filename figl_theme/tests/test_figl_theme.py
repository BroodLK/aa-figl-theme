"""
Figl Theme Test
"""

# Standard Library
from pathlib import Path

# Django
from django.test import TestCase
from django.urls import reverse


class TestFiglTheme(TestCase):
    """
    TestFiglTheme
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Test setup
        :return:
        :rtype:
        """

        super().setUpClass()

    def test_figl_theme(self):
        """
        Dummy test function
        :return:
        :rtype:
        """

        self.assertEqual(True, True)

    def test_notifications_count_url_uses_current_route_signature(self):
        template_path = (
            Path(__file__).resolve().parents[1]
            / "templates"
            / "allianceauth"
            / "base-bs5.html"
        )
        template_source = template_path.read_text(encoding="utf-8")

        self.assertEqual(
            reverse("notifications:user_notifications_count"),
            "/user_notifications_count/",
        )
        self.assertIn(
            "{% url 'notifications:user_notifications_count' %}",
            template_source,
        )
        self.assertNotIn(
            "{% url 'notifications:user_notifications_count' request.user.pk %}",
            template_source,
        )
