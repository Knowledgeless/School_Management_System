from django.apps import AppConfig


class SchoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'School'

    def ready(self):
        import School.signals  # Ensure signals are imported

