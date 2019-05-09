from django.core.management.base import BaseCommand
from old.models import (
    Users as OldUsers,
    Companies as OldCompanies,
    Clients as OldClients,
    Projects as OldProjects,
    Quotations as OldQuoatations,
    ProjectHasFiles as OldProjectFiles,
    ProjectHasActivities as OldProjectActivity,
    ProjectHasWorkers as OldProjectWorker,
    Invoices as OldInvoices,
    InvoiceHasItems as OldInvoiceItems,
)
from core.models import Postcodes
from accounts.models import User, Clients, Company
from projects.models import (
    Project,
    ProjectActivity,
    Invoice,
    InvoiceItems
)
from quotation.models import Quotation, TargetArea
from .helpers import (
    new_password,
    old_new_type_service,
    get_page_orientation,
    get_page_format,
    get_gsm,
    get_pages,
    get_color,
    get_processing,
    validate_date,
    validate_number,
    project_name_to_data,
    get_time,
    get_status,
    get_priority,
    unix_to_django_time,
    user_has_no_client,
    get_invoice_status,
    get_quote_status,
)
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

    def migrate_staffuser(self, olduser):
        npassword = new_password(olduser.hashed_password)
        if not User.objects.filter(email=olduser.email).exists():
            user = User.objects.create_staffuser(
                olduser.email,
                olduser.firstname,
                olduser.lastname,
                None
            )
            user.password = npassword
            user.save()
            self.old_new_log['users'].append({
                'old': olduser.pk,
                'new': user.pk
            })
            self.stdout.write(self.style.SUCCESS(
                'Created User name %s' % olduser.firstname))

    def migrate_projects(self, old_projects, company):
        for old_project in old_projects:
            if not Project.objects.filter(old_id=old_project.pk).exists():
                data = project_name_to_data(old_project.name)

                old_worker = OldProjectWorker.objects.using(
                    'old').filter(project_id=old_project.pk)
                if old_worker.exists():
                    worker = self.new_to_old_client(old_worker[0].user_id)
                    print(worker)
                else:
                    worker = None
                    print(old_project.pk)

                project = Project(
                    company=company,
                    project_admin=worker,
                    type_of_service=data['service'],
                    type_of_media=data['media'],
                    quantity_of_flyers=data['number'],

                    campaign_details=old_project.description,
                    campaign_start_date=validate_date(old_project.start),
                    campaign_finish_date=validate_date(old_project.end),
                    progress=validate_number(old_project.progress_calc),
                    created=old_project.datetime,
                    enable_client_tasks=old_project.enable_client_tasks,
                    hide_tasks=old_project.hide_tasks,
                    time_spent=get_time(old_project.time_spent),
                    note=old_project.note,
                    status=get_status(old_project.status),
                    priority=get_priority(old_project.priority),
                    old_id=old_project.pk
                )

                project.save()

                if old_project.postcodes:
                    postcodes = old_project.postcodes.split(',')

                    for postcode in postcodes:
                        po = Postcodes.objects.filter(full_name=postcode)
                        if po.exists():
                            project.target_postcodes.add(po[0])

                if old_project.area:
                    target_area = TargetArea(
                        households=validate_number(
                            data['number']),
                        geo_json=old_project.area
                    )
                    target_area.save()
                    project.target_area = target_area

                project.save()

                old_activities = OldProjectActivity.objects.using(
                    'old').filter(project_id=old_project.pk)

                for old_activity in old_activities:
                    if old_activity.user_id:
                        user = worker
                    else:
                        user = company.primary_user.user

                    activity = ProjectActivity(
                        project=project,
                        user=user,
                        created=unix_to_django_time(old_activity.datetime),
                        subject=old_activity.subject,
                        message=old_activity.message,
                        acitivity_type=old_activity.type,
                    )
                    activity.save()

    def migrate_company_clients(self, old_client):
        old_company = OldCompanies.objects.using(
            'old').filter(pk=old_client.company_id)
        if old_company.exists():
            old_company = OldCompanies.objects.using(
                'old').get(pk=old_client.company_id)
            if OldCompanies.objects.using('old').filter(
                    pk=old_client.company_id).exists():
                if User.objects.filter(email=old_client.email).exists():
                    user = User.objects.get(email=old_client.email)
                else:
                    user = User.objects.create_clientuser(
                        old_client.email,
                        old_client.firstname,
                        old_client.lastname,
                        None
                    )

                    user.password = new_password(old_client.hashed_password)
                    user.save()

                if user_has_no_client(user):
                    client = Clients(
                        user=user,
                        phone=old_client.phone,
                        mobile=old_client.mobile,
                        address=old_client.address,
                        postcode=old_client.zipcode,
                        city=old_client.city
                    )

                    client.save()

                    company = Company(
                        company_name=old_company.name,
                        primary_user=client,
                        address=old_company.address,
                        city=old_company.city,
                        postcode=old_company.zipcode,
                        vat=old_company.vat,
                        website=old_company.website,
                        country=old_company.country,
                        note=old_company.note,
                        terms=old_company.terms,
                    )
                    company.save()

                    client.company = company

                    client.save()
                else:
                    client = user.clients
                    company = client.company

                old_projects = OldProjects.objects.using(
                    'old').filter(company_id=old_company.pk)

                self.old_new_log['company'].append({
                    'old': old_company.pk,
                    'new': company.pk
                })

                self.old_new_log['clients'].append({
                    'old': old_client.pk,
                    'new': client.pk
                })

                self.migrate_projects(old_projects, company)

    def migrate_quotation(self, old_quotation):
        if not old_quotation.cost:
            old_quotation.cost = 0
        else:
            old_quotation.cost = old_quotation.cost.replace(',', '')
        quotation = Quotation(
            business_name=old_quotation.company,
            full_name=old_quotation.fullname,
            email=old_quotation.email,
            phone=old_quotation.phone,
            postcode=old_quotation.zip,
            street=old_quotation.address,
            city=old_quotation.city,
            type_of_service=old_new_type_service(old_quotation.q1),
            number_of_boxes=validate_number(old_quotation.q6),
            type_of_media=validate_number(old_quotation.q2),
            require_collection=validate_number(old_quotation.q3),
            quantity_of_flyers=validate_number(
                old_quotation.q4.replace(',', '')),
            title_of_media=old_quotation.media_title,
            campaign_details=old_quotation.q5,
            agreed_cost=validate_number(old_quotation.cost),
            campaign_start_date=validate_date(old_quotation.start),
            campaign_finish_date=validate_date(old_quotation.country),
            special_instruction=old_quotation.comment,
            account_manager=self.get_refer(old_quotation.refer),
            status=get_quote_status(old_quotation.status),
            issued_date=old_quotation.date,
            old_id=old_quotation.pk,
            assigned_user=self.new_to_old_client(old_quotation.user_id),
        )
        print(quotation.issued_date)
        quotation.save()

        print("%s  %s" % (quotation.business_name, old_quotation.pk))

        if old_quotation.pages:
            quotation.printing_required = True
            quotation.pages = get_pages(
                old_quotation.pages)
            quotation.page_orientation = get_page_orientation(
                old_quotation.page_orien)
            quotation.page_format = get_page_format(
                old_quotation.page_format)
            quotation.gsm = get_gsm(
                old_quotation.page_paper)
            quotation.colours = get_color(old_quotation.page_color)
            quotation.processing = get_processing(old_quotation.page_proc)
        if old_quotation.target_postcodes:
            postcodes = old_quotation.target_postcodes.split(',')

            for postcode in postcodes:
                po = Postcodes.objects.filter(full_name=postcode)
                if po.exists():
                    quotation.target_postcodes.add(po[0])

        if old_quotation.target_area:
            target_area = TargetArea(
                households=validate_number(
                    old_quotation.q4.replace(',', '')),
                geo_json=old_quotation.target_area
            )
            target_area.save()
            quotation.target_area = target_area

        quotation.save()

    def migrate_invoices(self, old_invoice):
        if not Invoice.objects.filter(old_id=old_invoice.pk).exists():
            company = self.new_to_old_company(old_invoice.company_id)

            if old_invoice.project_id and Project.objects.filter(
                    old_id=old_invoice.project_id).exists():
                project = Project.objects.get(old_id=old_invoice.project_id)
            else:
                project = None
            invoice = Invoice(
                company=company,
                project=project,
                sent_date=validate_date(old_invoice.sent_date),
                issue_date=validate_date(old_invoice.issue_date),
                due_date=validate_date(old_invoice.due_date),
                paid_date=validate_date(old_invoice.paid_date),
                terms=old_invoice.terms,
                discount=validate_number(old_invoice.discount),
                tax=validate_number(old_invoice.tax),
                total=validate_number(old_invoice.sum),
                status=get_invoice_status(old_invoice.status),
                second_tax=validate_number(old_invoice.second_tax),
                po_number=old_invoice.po_number,
                paid=validate_number(old_invoice.paid),
                outstanding=validate_number(old_invoice.outstanding),
                old_id=old_invoice.pk
            )
            invoice.save()
            old_invoice_items = OldInvoiceItems.objects.using(
                'old').filter(invoice_id=old_invoice.pk)
            for old_item in old_invoice_items:
                invoice_item = InvoiceItems(
                    invoice=invoice,
                    amount=validate_number(old_item.amount),
                    description=old_item.description,
                    value=validate_number(old_item.value),
                    name=old_item.name,
                    item_type=old_item.type,
                )
                invoice_item.save()

    def handle(self, *args, **options):
        # users = OldUsers.objects.using('old').all()
        # for user in users:
        #     self.migrate_staffuser(user)
        # print(self.old_new_log)

        # with open('data.json', 'w') as outfile:
        #     json.dump(self.old_new_log, outfile)

        quotations = OldQuoatations.objects.using('old').all()

        for q in quotations:
            self.migrate_quotation(q)

        # old_clients = OldClients.objects.using('old').all()

        # for old_client in old_clients:
        #     self.migrate_company_clients(old_client)

        # with open('data.json', 'w') as outfile:
        #     json.dump(self.old_new_log, outfile)

        # old_invoices = OldInvoices.objects.using('old').all()

        # for old_invoice in old_invoices:
        #     self.migrate_invoices(old_invoice)

        # with open('data.json', 'w') as outfile:
        #     json.dump(self.old_new_log, outfile)

    def new_to_old_client(self, old_id):
        for ids in self.old_new_log['users']:
            if ids['old'] == old_id:
                return User.objects.get(pk=ids['new'])
        return None

    def new_to_old_company(self, old_id):
        for ids in self.old_new_log['company']:
            if int(ids['old']) == int(old_id):
                return Company.objects.get(pk=ids['new'])
        return None

    def get_refer(self, first_name):
        if not first_name:
            return None
        user = User.objects.filter(first_name=first_name)[0]
        user.accountant = True
        user.save()
        return user
