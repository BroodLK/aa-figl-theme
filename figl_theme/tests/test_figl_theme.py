"""
Figl Theme Test
"""

# Django
from django.test import TestCase


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
