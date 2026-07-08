import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create the beta test access account if it does not exist (idempotent)'

    def handle(self, *args, **options):
        email = os.environ.get('GUEST_USER_EMAIL', 'beta@nvlp.app')
        password = os.environ.get('GUEST_USER_PASSWORD', 'nvlp-beta-access')

        User = get_user_model()
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': 'Beta',
                'last_name': 'Tester',
                'role': 'student',
            },
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created beta test account {email}'))
        else:
            self.stdout.write(f'Beta test account {email} already exists')
