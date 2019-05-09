from quotation.models import Quotation
from django.core.management.base import BaseCommand
from accounts.models import User, Clients, Company
from projects.models import Project, Invoice
from quotation.models import Quotation


class Command(BaseCommand):
    help = "Testing Command "
    old_new_log = {
        'users': [
        ]
    }

    def handle(self, *args, **options):
        # User.objects.all().delete()
        # Clients.objects.all().delete()
        # Company.objects.all().delete()
        # Project.objects.all().delete()
        # Invoice.objects.all().delete()
        Quotation.objects.all().delete()
