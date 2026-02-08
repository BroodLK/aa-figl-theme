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
    'figl_theme',
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

## Notes

- The template override adds the top info header (EVE time, killboard, Dotlan) and customizes the main navbar.
- "Add Character" routes to `/audit/char/add/` via a template override.
