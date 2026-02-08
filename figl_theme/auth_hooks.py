"""Hook into Alliance Auth"""

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import UrlHook
from allianceauth.theme.hooks import ThemeHook

# AA Figl Theme
from figl_theme import urls

@hooks.register("url_hook")
def register_urls():
    """Register app urls"""

    return UrlHook(urls, "figl_theme", r"^figl_theme/")


class FiglThemeHook(ThemeHook):
    """Theme hook to load the Figl Theme styling."""

    def __init__(self):
        ThemeHook.__init__(
            self,
            "Figl Theme",
            "Sci-fi teal and red theme inspired by Flying Dangerous.",
            css=[],
            js=[],
            css_template="figl_theme/theme_css.html",
            js_template="figl_theme/theme_js.html",
            html_tags={"data-theme": "figl-theme", "data-bs-theme": "dark"},
            header_padding="6em",
        )


@hooks.register("theme_hook")
def register_figl_theme_hook():
    """Register theme hook."""

    return FiglThemeHook()
