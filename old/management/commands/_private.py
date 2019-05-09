from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Testing Command "

    def handle(self, *args, **options):
        pass
