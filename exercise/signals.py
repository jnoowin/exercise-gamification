from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import Dashboard, QuestCompleted

'''
Title: Signals
https://django-allauth.readthedocs.io/en/latest/signals.html
'''
@receiver(user_signed_up)
def init_dashboard(request, user, **kwargs):
    dashboard = Dashboard(user=user)
    dashboard.save()
    qc = QuestCompleted(user=user)
    qc.save()
