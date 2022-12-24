from django.apps import AppConfig
from allauth.account.signals import user_signed_up

class ExerciseConfig(AppConfig):
    name = 'exercise'

    def ready(self):
        import exercise.signals
