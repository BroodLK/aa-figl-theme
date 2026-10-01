"""
Figl Theme Test
"""

# Standard Library
from pathlib import Path
from unittest.mock import patch

# Django
from django.template import Context, Template
from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase, override_settings

# AA Figl Theme
from figl_theme import app_settings
from figl_theme.auth_hooks import FiglThemeHook
from figl_theme.templatetags import figl_theme_tags


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

    def test_figl_theme_hook_properties(self):
        hook = FiglThemeHook()
        self.assertEqual(hook.name, "Figl Theme")
        self.assertEqual(hook.css_template, "figl_theme/theme_css.html")
        self.assertEqual(hook.js_template, "figl_theme/theme_js.html")
        self.assertEqual(hook.html_tags, "data-theme=figl-theme data-bs-theme=dark")

    def test_app_settings_defaults(self):
        self.assertTrue(app_settings.FIGL_ENABLE_EVE_TIME)
        self.assertTrue(app_settings.FIGL_GLOW_EFFECTS)
        self.assertIsInstance(app_settings.FIGL_HEADER_LINKS, list)
        self.assertEqual(len(app_settings.FIGL_HEADER_LINKS), 4)
        self.assertEqual(
            app_settings.FIGL_DEV_SUPPORT_URL, "https://ko-fi.com/biobrute"
        )
        self.assertEqual(app_settings.FIGL_DEV_SUPPORT_TEXT, "Support the Dev")
        self.assertIsNone(app_settings.FIGL_BG_IMAGE_URL)
        self.assertIsNone(app_settings.FIGL_LOGIN_VIDEO_URL)
        self.assertIsNone(app_settings.FIGL_LOGIN_BG_IMAGE_URL)

    def test_templatetags_defaults(self):
        self.assertTrue(figl_theme_tags.figl_enable_eve_time())
        self.assertTrue(figl_theme_tags.figl_glow_effects())
        self.assertIsInstance(figl_theme_tags.figl_header_links(), list)
        self.assertEqual(
            figl_theme_tags.figl_dev_support_url(), "https://ko-fi.com/biobrute"
        )
        self.assertEqual(figl_theme_tags.figl_dev_support_text(), "Support the Dev")
        self.assertEqual(figl_theme_tags.figl_bg_image_url(), "")
        self.assertEqual(figl_theme_tags.figl_login_video_url(), "")
        self.assertEqual(figl_theme_tags.figl_login_bg_image_url(), "")

    @override_settings(
        FIGL_ENABLE_EVE_TIME=False,
        FIGL_HEADER_LINKS=[{"label": "Custom", "url": "https://custom.example.com"}],
        FIGL_DEV_SUPPORT_URL=None,
        FIGL_DEV_SUPPORT_TEXT="Custom Dev Text",
        FIGL_GLOW_EFFECTS=False,
        FIGL_BG_IMAGE_URL="/static/figl_theme/img/auth_bg.jpg",
        FIGL_LOGIN_VIDEO_URL="/static/figl_theme/video/eve.mp4",
        FIGL_LOGIN_BG_IMAGE_URL="/static/figl_theme/img/poster.jpg",
    )
    def test_templatetags_overrides(self):
        self.assertFalse(figl_theme_tags.figl_enable_eve_time())
        self.assertFalse(figl_theme_tags.figl_glow_effects())
        self.assertEqual(
            figl_theme_tags.figl_header_links(),
            [{"label": "Custom", "url": "https://custom.example.com"}],
        )
        self.assertIsNone(figl_theme_tags.figl_dev_support_url())
        self.assertEqual(figl_theme_tags.figl_dev_support_text(), "Custom Dev Text")
        self.assertEqual(
            figl_theme_tags.figl_bg_image_url(), "/static/figl_theme/img/auth_bg.jpg"
        )
        self.assertEqual(
            figl_theme_tags.figl_login_video_url(), "/static/figl_theme/video/eve.mp4"
        )
        self.assertEqual(
            figl_theme_tags.figl_login_bg_image_url(),
            "/static/figl_theme/img/poster.jpg",
        )

    def test_theme_css_and_js_templates_rendered(self):
        css_rendered = render_to_string("figl_theme/theme_css.html")
        self.assertIn("cdnjs.cloudflare.com/ajax/libs/bootstrap", css_rendered)
        self.assertIn("cdnjs.cloudflare.com/ajax/libs/font-awesome", css_rendered)
        self.assertIn("figl_theme/css/figl-theme.css", css_rendered)
        self.assertIn("fonts.googleapis.com", css_rendered)

        js_rendered = render_to_string("figl_theme/theme_js.html")
        self.assertIn("cdnjs.cloudflare.com/ajax/libs/popper", js_rendered)
        self.assertIn("cdnjs.cloudflare.com/ajax/libs/bootstrap", js_rendered)

    def test_base_template_customization(self):
        template_content = """
        {% load figl_theme_tags %}
        {% figl_enable_eve_time as show_eve_time %}
        {% figl_header_links as header_links %}
        {% figl_dev_support_url as support_url %}
        {% if show_eve_time %}SHOW_CLOCK{% endif %}
        {% for l in header_links %}{{ l.label }}|{{ l.url }};{% endfor %}
        {% if support_url %}{{ support_url }}{% endif %}
        """
        t = Template(template_content)

        # Default settings
        rendered = t.render(Context({}))
        self.assertIn("SHOW_CLOCK", rendered)
        self.assertIn("KillBoard|https://zkillboard.com/alliance/99009902/", rendered)
        self.assertIn("https://ko-fi.com/biobrute", rendered)

        # Overridden settings
        with self.settings(
            FIGL_ENABLE_EVE_TIME=False,
            FIGL_HEADER_LINKS=[{"label": "TestLink", "url": "https://example.com"}],
            FIGL_DEV_SUPPORT_URL=None,
        ):
            rendered_override = t.render(Context({}))
            self.assertNotIn("SHOW_CLOCK", rendered_override)
            self.assertIn("TestLink|https://example.com", rendered_override)
            self.assertNotIn("https://ko-fi.com/biobrute", rendered_override)

    def test_notifications_count_url_uses_current_route_signature(self):
        template_path = (
            Path(__file__).resolve().parents[1]
            / "templates"
            / "allianceauth"
            / "base-bs5.html"
        )
        template_source = template_path.read_text(encoding="utf-8")

        self.assertIn(
            "{% figl_notifications_count_url %}",
            template_source,
        )

        class DummyUser:
            pk = 1

        context = Context({"user": DummyUser()})

        # Test resolving in current environment (takes user_pk)
        resolved_url = figl_theme_tags.figl_notifications_count_url(context)
        self.assertEqual(resolved_url, "/user_notifications_count/1/")

        # Test resolving when 0-arg reverse succeeds (newer Alliance Auth)
        with patch("figl_theme.templatetags.figl_theme_tags.reverse") as mock_reverse:
            mock_reverse.return_value = "/user_notifications_count/"
            url_zero_args = figl_theme_tags.figl_notifications_count_url(context)
            self.assertEqual(url_zero_args, "/user_notifications_count/")
            mock_reverse.assert_called_with("notifications:user_notifications_count")

    def test_figl_theme_css_modernization_rules(self):
        css_path = (
            Path(__file__).resolve().parents[1]
            / "static"
            / "figl_theme"
            / "css"
            / "figl-theme.css"
        )
        css_content = css_path.read_text(encoding="utf-8")

        # Tabular nums & Typography
        self.assertIn("tabular-nums", css_content)
        self.assertIn("clamp(", css_content)
        self.assertIn("JetBrains Mono", css_content)

        # Glassmorphism & Elevation
        self.assertIn("backdrop-filter: blur(", css_content)

        # Sticky table headers
        self.assertIn("position: sticky", css_content)

        # Standings & Threat Recognition Palette
        self.assertIn(".standing-excellent", css_content)
        self.assertIn(".standing-terrible", css_content)
        self.assertIn("color-mix(", css_content)

        # Modern SaaS Theme styling & rules
        self.assertIn("pulse-hud", css_content)
        self.assertIn("::selection", css_content)
        self.assertIn(".tooltip-inner", css_content)
        self.assertIn("#aa-user-info", css_content)
        self.assertIn("border-left: 3px solid", css_content)
        self.assertIn(".progress-bar", css_content)
        self.assertIn("--figl-teal: #229388", css_content)
        self.assertIn("#sidebar-menu .badge", css_content)
        self.assertIn("#sidebar-menu span.pill", css_content)
        self.assertIn("#sidebar-menu .collapse", css_content)
        self.assertIn(".navbar .navbar-brand[data-bs-toggle] .badge", css_content)

        # Login Screen & Video Background styling
        self.assertIn(".figl-login-video-bg", css_content)
        self.assertIn(".figl-login-video", css_content)
        self.assertIn(".figl-login-video-overlay", css_content)
        self.assertIn(".figl-login-card", css_content)
        self.assertIn(".card-login", css_content)

        # Content Background styling
        self.assertIn("body.has-figl-bg", css_content)
        self.assertIn("--figl-bg-image", css_content)

        # Community App Component compatibility styling (Select2, DataTables, Accordion, Code)
        self.assertIn(".select2-container--default", css_content)
        self.assertIn(".select2-dropdown", css_content)
        self.assertIn(".dataTables_wrapper", css_content)
        self.assertIn(".accordion-item", css_content)

    def test_base_template_bg_image_rendered(self):
        rf = RequestFactory()
        request = rf.get("/")

        # Default rendering without background image
        base_rendered = render_to_string(
            "allianceauth/base-bs5.html", {"request": request}
        )
        self.assertNotIn("has-figl-bg", base_rendered)
        self.assertNotIn("--figl-bg-image", base_rendered)

        # Rendering with FIGL_BG_IMAGE_URL configured
        with self.settings(FIGL_BG_IMAGE_URL="/static/figl_theme/img/auth_bg.jpg"):
            base_bg_rendered = render_to_string(
                "allianceauth/base-bs5.html", {"request": request}
            )
            self.assertIn("has-figl-bg", base_bg_rendered)
            self.assertIn("/static/figl_theme/img/auth_bg.jpg", base_bg_rendered)
            self.assertIn("--figl-bg-image", base_bg_rendered)

    def test_public_login_template_rendered(self):
        # Default rendering without video setting
        login_rendered = render_to_string("public/login.html", {"request": None})
        self.assertIn("figl-login-video-bg", login_rendered)
        self.assertIn("figl-login-video", login_rendered)
        self.assertIn("figl-login-card", login_rendered)
        self.assertIn("data-theme=figl-theme", login_rendered)

        # Rendering with video and poster settings configured
        with self.settings(
            FIGL_LOGIN_VIDEO_URL="/static/figl_theme/video/eve_space.mp4",
            FIGL_LOGIN_BG_IMAGE_URL="/static/figl_theme/img/login_poster.jpg",
        ):
            login_video_rendered = render_to_string(
                "public/login.html", {"request": None}
            )
            self.assertIn(
                'src="/static/figl_theme/video/eve_space.mp4"', login_video_rendered
            )
            self.assertIn(
                'poster="/static/figl_theme/img/login_poster.jpg"', login_video_rendered
            )
