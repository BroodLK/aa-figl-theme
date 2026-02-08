"""App Configuration"""

# Django
from django.apps import AppConfig

# AA Figl Theme
from figl_theme import __version__


class FiglThemeConfig(AppConfig):
    """App Config"""

    name = "figl_theme"
    label = "figl_theme"
    verbose_name = f"Figl Theme v{__version__}"
