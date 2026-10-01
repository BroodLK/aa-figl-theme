"""Template tags for Figl Theme."""

# Django
from django import template
from django.conf import settings
from django.urls import NoReverseMatch, reverse

# AA Figl Theme
from figl_theme import app_settings

register = template.Library()


@register.simple_tag
def figl_enable_eve_time() -> bool:
    """Return whether EVE time clock is enabled in top info header."""
    return getattr(settings, "FIGL_ENABLE_EVE_TIME", app_settings.FIGL_ENABLE_EVE_TIME)


@register.simple_tag
def figl_header_links() -> list:
    """Return header links configured for top info header."""
    return getattr(settings, "FIGL_HEADER_LINKS", app_settings.FIGL_HEADER_LINKS)


@register.simple_tag
def figl_dev_support_url() -> str:
    """Return dev support URL or empty string/None."""
    return getattr(settings, "FIGL_DEV_SUPPORT_URL", app_settings.FIGL_DEV_SUPPORT_URL)


@register.simple_tag
def figl_dev_support_text() -> str:
    """Return dev support button text."""
    return getattr(
        settings, "FIGL_DEV_SUPPORT_TEXT", app_settings.FIGL_DEV_SUPPORT_TEXT
    )


@register.simple_tag
def figl_glow_effects() -> bool:
    """Return whether glow visual effects are enabled."""
    return getattr(settings, "FIGL_GLOW_EFFECTS", app_settings.FIGL_GLOW_EFFECTS)


@register.simple_tag
def figl_bg_image_url() -> str:
    """Return configured content/auth background image URL if set."""
    return (
        getattr(
            settings,
            "FIGL_BG_IMAGE_URL",
            getattr(
                settings, "FIGL_BACKGROUND_IMAGE_URL", app_settings.FIGL_BG_IMAGE_URL
            ),
        )
        or ""
    )


@register.simple_tag
def figl_login_video_url() -> str:
    """Return configured login background video URL if set."""
    return (
        getattr(settings, "FIGL_LOGIN_VIDEO_URL", app_settings.FIGL_LOGIN_VIDEO_URL)
        or ""
    )


@register.simple_tag
def figl_login_bg_image_url() -> str:
    """Return configured login background fallback image URL if set."""
    return (
        getattr(
            settings, "FIGL_LOGIN_BG_IMAGE_URL", app_settings.FIGL_LOGIN_BG_IMAGE_URL
        )
        or ""
    )


@register.simple_tag(takes_context=True)
def figl_notifications_count_url(context) -> str:
    """Resolve notification count URL with fallback across Alliance Auth versions."""
    request = context.get("request")
    user = getattr(request, "user", None) or context.get("user")
    user_pk = getattr(user, "pk", None)

    # Newer Alliance Auth (4.x+): user_notifications_count has no URL args
    try:
        return reverse("notifications:user_notifications_count")
    except NoReverseMatch:
        pass

    # Older Alliance Auth: user_notifications_count requires user_pk
    if user_pk is not None:
        try:
            return reverse("notifications:user_notifications_count", args=[user_pk])
        except NoReverseMatch:
            pass

    return ""
