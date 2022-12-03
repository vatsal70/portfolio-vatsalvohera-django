# __init__ file

from .celery_v2 import app as celery_app

__all__ = ('celery_app',)