import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create the demo and admin accounts if they do not exist (idempotent)'

    def handle(self, *args, **options):
        User = get_user_model()

        email = os.environ.get('DEMO_USER_EMAIL', 'demo@nvlp.app')
        password = os.environ.get('DEMO_USER_PASSWORD', 'nvlp-demo-2026')

        user, created = User.objects.get_or_create(email=email)
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created demo user {email}'))
        else:
            self.stdout.write(f'Demo user {email} already exists')

        # Admin account: only seeded when credentials are provided via
        # environment, so the password never lives in the repository
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@nvlp.app')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        if not admin_password:
            self.stdout.write('ADMIN_PASSWORD not set; skipping admin account')
            return

        admin, created = User.objects.get_or_create(email=admin_email)
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True
        # Always reset the password so changing the env var updates the
        # account on the next restart
        admin.set_password(admin_password)
        admin.save()
        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'{action} admin account {admin_email}'))
