from __future__ import unicode_literals

from django.apps import AppConfig


class ApphomeConfig(AppConfig):
    name = 'app_core'
    verbose_name = 'app_core'

    def ready(self):
        import app_core.signals
