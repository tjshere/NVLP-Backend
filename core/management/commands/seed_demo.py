import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create the demo login account if it does not exist (idempotent)'

    def handle(self, *args, **options):
        email = os.environ.get('DEMO_USER_EMAIL', 'demo@nvlp.app')
        password = os.environ.get('DEMO_USER_PASSWORD', 'nvlp-demo-2026')

        User = get_user_model()
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created demo user {email}'))
        else:
            self.stdout.write(f'Demo user {email} already exists')
