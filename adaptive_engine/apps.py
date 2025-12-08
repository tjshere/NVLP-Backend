from django.apps import AppConfig


class AdaptiveEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adaptive_engine'
    
    def ready(self):
        """
        Import and register signals when the app is ready.
        """
        import adaptive_engine.signals