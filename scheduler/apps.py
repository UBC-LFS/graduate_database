from django.conf import settings
from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        if settings.DEBUG == False:
            from scheduler import tasks
            tasks.run()