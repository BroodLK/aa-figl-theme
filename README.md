# Figl Theme for Alliance Auth

Sci-fi teal and red theme inspired by Flying Dangerous.

## Requirements

- Alliance Auth 4.x (tested with 4.12)
- Django 4.2+

## Install (AA project)

Update your AA settings (e.g. `myauth/settings/local.py`):

```python
import os
from pathlib import Path

import figl_theme

INSTALLED_APPS += [
    "figl_theme",
]

DEFAULT_THEME = "figl_theme.auth_hooks.FiglThemeHook"
DEFAULT_THEME_DARK = DEFAULT_THEME

FIGL_THEME_TEMPLATES = Path(figl_theme.__file__).resolve().parent / "templates"
TEMPLATES[0]["DIRS"].insert(0, str(FIGL_THEME_TEMPLATES))
```

Collect static files and restart AA:

```bash
python manage.py collectstatic
```

## Configuration (Optional)

You can customize the theme behavior in your `local.py`:

```python
# Enable/disable EVE time clock in the top info header (default: True)
FIGL_ENABLE_EVE_TIME = True

# Customize header quick links (default: KillBoard, Dotlan, Merch Store, Wiki)
FIGL_HEADER_LINKS = [
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
    {"label": "Wiki", "url": "https://wiki.figl.us/", "target": "_blank"},
]

# Customize or disable developer support link
FIGL_DEV_SUPPORT_URL = "https://ko-fi.com/biobrute"
FIGL_DEV_SUPPORT_TEXT = "Support the Dev"

# Glow visual effects toggle (default: True)
FIGL_GLOW_EFFECTS = True

# Main auth content background image (e.g. in-game wallpaper/nebula)
FIGL_BG_IMAGE_URL = "/static/figl_theme/img/auth_bg.jpg"

# Login screen background video (e.g. in-game capture mp4) & fallback poster
FIGL_LOGIN_VIDEO_URL = "/static/figl_theme/video/login_bg.mp4"  # or remote URL
FIGL_LOGIN_BG_IMAGE_URL = "/static/figl_theme/img/login_poster.jpg"
```

## Notes

- The template override adds the top info header (EVE time, killboard, Dotlan) and customizes the main navbar.
- The authenticated auth content supports a custom background image (`FIGL_BG_IMAGE_URL`) with an automated high-contrast overlay for dashboard legibility.
- The public login screen is themed with Figl styling and supports full-viewport in-game video backgrounds (`FIGL_LOGIN_VIDEO_URL`) with fallback posters (`FIGL_LOGIN_BG_IMAGE_URL`).
- "Add Character" routes to `/audit/char/add/` via a template override.
