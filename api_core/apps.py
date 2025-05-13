from django.apps import AppConfig


class ApiCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_core'
# api_core/apps.py
def ready(self):
    import api_core.signals
