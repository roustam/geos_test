from typing import Any
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User;

class Command(BaseCommand):
    help = 'Script that creates admin user if it does not exist with pw 123qwe'

    def handle(self, *args, **options) -> None:
        if not User.objects.count():
            User.objects.create_superuser('admin', 'admin@example.com', '123qwe')
 #test