"""App Settings"""

# Django
from django.conf import settings

# put your app settings here


FIGL_THEME_SETTING_ONE = getattr(settings, "FIGL_THEME_SETTING_ONE", None)
