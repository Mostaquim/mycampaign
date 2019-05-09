from django.core.management.base import BaseCommand
from .helpers import unix_to_django_time
from accounts.models import User, Company, Clients
import json


class Command(BaseCommand):
    help = "Testing Command "

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        try:
            with open('data.json', "r") as outfile:
                self.old_new_log = json.load(outfile)

        except:
            self.old_new_log = {
                'users': [
                ],
                'company': [],
                'clients': [],
                'projects': []
            }

    def handle(self, *args, **options):
        unix_to_django_time(1554911425)
        unix_to_django_time(1551275414)

        u = self.new_to_old_client(169)
        c = self.new_to_old_company(34)
        print(c)

    def new_to_old_client(self, old_id):
        for ids in self.old_new_log['users']:
            if int(ids['old']) == int(old_id):
                return User.objects.get(pk=ids['new'])

        return None

    def new_to_old_company(self, old_id):
        for ids in self.old_new_log['users']:
            if int(ids['old']) == int(old_id):
                return Company.objects.get(pk=ids['new'])

        return None
