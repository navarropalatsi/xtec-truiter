from django.apps import AppConfig


class XarxaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xarxa'

    def ready(self):
        # Importa els signals quan l'app estigui preparada
        import xarxa.signals
