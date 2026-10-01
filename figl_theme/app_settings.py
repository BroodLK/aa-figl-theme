"""App Settings for Figl Theme."""

# Django
from django.conf import settings

# EVE Time clock display toggle
FIGL_ENABLE_EVE_TIME: bool = getattr(settings, "FIGL_ENABLE_EVE_TIME", True)

# Default links displayed in top info header
DEFAULT_FIGL_HEADER_LINKS = [
    {
        "label": "KillBoard",
        "url": "https://zkillboard.com/alliance/99009902/",
        "target": "_blank",
    },
    {
        "label": "Dotlan",
        "url": "https://evemaps.dotlan.net/alliance/Flying%20Dangerous",
        "target": "_blank",
    },
    {
        "label": "Merch Store",
        "url": "https://flying-dangerous-shop.fourthwall.com/",
        "target": "_blank",
    },
    {
        "label": "Wiki",
        "url": "https://wiki.figl.us/",
        "target": "_blank",
    },
]

FIGL_HEADER_LINKS = getattr(settings, "FIGL_HEADER_LINKS", DEFAULT_FIGL_HEADER_LINKS)

# Support / donation link
FIGL_DEV_SUPPORT_URL = getattr(
    settings, "FIGL_DEV_SUPPORT_URL", "https://ko-fi.com/biobrute"
)
FIGL_DEV_SUPPORT_TEXT = getattr(settings, "FIGL_DEV_SUPPORT_TEXT", "Support the Dev")

# Glow visual effects toggle
FIGL_GLOW_EFFECTS: bool = getattr(settings, "FIGL_GLOW_EFFECTS", True)

# Content / Authenticated background image setting
FIGL_BG_IMAGE_URL = getattr(
    settings, "FIGL_BG_IMAGE_URL", getattr(settings, "FIGL_BACKGROUND_IMAGE_URL", None)
)

# Login screen background video & image settings
FIGL_LOGIN_VIDEO_URL = getattr(settings, "FIGL_LOGIN_VIDEO_URL", None)
FIGL_LOGIN_BG_IMAGE_URL = getattr(settings, "FIGL_LOGIN_BG_IMAGE_URL", None)
