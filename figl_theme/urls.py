"""App URLs"""

# Django
from django.urls import path

# AA Figl Theme
from figl_theme import views

app_name: str = "figl_theme"  # pylint: disable=invalid-name

urlpatterns = [
    path("", views.index, name="index"),
]
