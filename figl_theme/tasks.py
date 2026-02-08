"""App Tasks"""

# Standard Library
import logging

# Third Party
from celery import shared_task

logger = logging.getLogger(__name__)

# Create your tasks here


# Figl Theme Task
@shared_task
def figl_theme_task():
    """Figl Theme Task"""

    pass
