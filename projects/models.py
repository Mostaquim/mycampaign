from django.db import models, transaction
from quotation.choices import *
from quotation.models import Quotation, GSM, Format, TargetArea
from accounts.models import User, Company, Clients
from core.models import Postcodes, Attachments
import datetime
from .choices import *


class ProjectManager(models.Manager):
    def generate(self, request, quotation):
        if request.user.is_staff:
            with transaction.atomic():
                client = Clients.objects.get_or_create_client(
                    quotation.business_name,
                    quotation.full_name,
                    quotation.phone,
                    quotation.email,
                    quotation.street,
                    quotation.city,
                    quotation.postcode
                )

                project_admin = User.objects.get(pk=1)

                project = self.model(
                    quotation=quotation,
                    company=client.company,
                    project_admin=project_admin,
                    type_of_service=quotation.type_of_service,
                    number_of_boxes=quotation.number_of_boxes,
                    type_of_media=quotation.type_of_media,
                    require_collection=quotation.require_collection,
                    quantity_of_flyers=quotation.quantity_of_flyers,
                    title_of_media=quotation.title_of_media,
                    campaign_details=quotation.campaign_details,
                    agreed_cost=quotation.agreed_cost,
                    campaign_start_date=quotation.campaign_start_date,
                    campaign_finish_date=quotation.campaign_finish_date,
                    special_instruction=quotation.special_instruction,
                )

                project.save()

                for postcodes in quotation.target_postcodes.all():
                    project.target_postcodes.add(postcodes)

                for attachments in quotation.attachments.all():
                    project.attachments.add(attachments)

                project.save()
                invoice = Invoice(
                    company=client.company,
                    project=project,
                    currency=1,
                    issue_date=datetime.date.today(),
                    due_date=datetime.date.today() + datetime.timedelta(
                        days=4),
                    terms=INVOICE_TERMS,
                    discount=0,
                    tax=.2,
                    total=0,
                    status=1,
                    second_tax=0
                )

                invoice.save()

                invoice_item = InvoiceItems(
                    invoice=invoice,
                    amount=quotation.quantity_of_flyers,
                    description='Leaflet Distribution',
                    value=quotation.agreed_cost,
                    name='Leaflet Distribution',
                    item_type='As per order form'
                )

                invoice_item.save()

                if quotation.printing_required:
                    printing_order = PrintingOrder(
                        quotation=quotation,
                        company=client.company,
                        project=project,
                        pages=quotation.pages,
                        page_orientation=quotation.page_orientation,
                        page_format=quotation.page_format,
                        gsm=quotation.gsm,
                        colours=quotation.colours,
                        processing=quotation.processing,
                    )

                    invoice_item = InvoiceItems(
                        invoice=invoice,
                        amount=quotation.quantity_of_flyers,
                        description='Printing Cost',
                        value=0,
                        name='Printing Cost',
                        item_type='Printing'
                    )

                    invoice_item.save()

                    printing_order.save()


# Create your models here.
class Project(models.Model):
    quotation = models.OneToOneField(
        Quotation,
        on_delete=models.SET_NULL,
        null=True,
        related_name="quotation"
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects",
    )

    project_admin = models.ForeignKey(
        User,
        limit_choices_to={'staff': True},
        on_delete=models.SET_NULL,
        null=True,
        related_name="project_admin"
    )

    type_of_service = models.IntegerField(
        choices=SERVICE_CHOICES,
        default=1,
        null=True
    )
    number_of_boxes = models.IntegerField(
        choices=BOX_TO_COLLECT,
        default=1,
        null=True
    )
    type_of_media = models.IntegerField(
        choices=TYPE_OF_MEDIA,
        default=1,
        null=True
    )
    require_collection = models.IntegerField(
        choices=REQUIRE_COLLECTION,
        default=1,
        null=True
    )

    # campaign details
    quantity_of_flyers = models.IntegerField(null=True, blank=False)
    title_of_media = models.CharField(max_length=255, null=True)
    campaign_details = models.TextField(max_length=255, null=True)
    agreed_cost = models.DecimalField(
        max_digits=11, decimal_places=2, null=True)
    campaign_start_date = models.DateField(null=True)
    campaign_finish_date = models.DateField(null=True)
    special_instruction = models.TextField(null=True)
    target_postcodes = models.ManyToManyField(
        Postcodes, related_name="target_postcodes", null=True)
    attachments = models.ManyToManyField(
        Attachments, null=True
    )
    progress = models.IntegerField(default=0)
    target_area = models.ForeignKey(
        TargetArea, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, null=True)

    # old fields
    enable_client_tasks = models.IntegerField(blank=True, null=True)
    hide_tasks = models.IntegerField(blank=True, null=True)
    time_spent = models.DurationField(null=True)
    note = models.TextField(null=True)
    status = models.IntegerField(choices=PROJECT_STATUS, default=1)
    priority = models.IntegerField(choices=PRIORITY, default=2)

    old_id = models.IntegerField(default=0)

    objects = ProjectManager()


class PrintingOrder(models.Model):
    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.SET_NULL,
        null=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True
    )
    pages = models.IntegerField(choices=PAGES)
    page_orientation = models.IntegerField(choices=PAGE_ORIENTATION)
    page_format = models.ForeignKey(
        Format, on_delete=models.SET_NULL, null=True)
    gsm = models.ForeignKey(GSM, on_delete=models.SET_NULL, null=True)
    colours = models.IntegerField(choices=COLORS)
    processing = models.IntegerField(choices=PROCESSING)
    created = models.DateTimeField(auto_now_add=True, null=True)


class Invoice(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        related_name="invoice_company"
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        related_name="invoice_project"
    )

    currency = models.IntegerField(choices=CURRENCY, default=1)
    sent_date = models.DateField(auto_now_add=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    paid_date = models.DateField(null=True)
    terms = models.TextField()
    discount = models.DecimalField(decimal_places=2, max_digits=11)
    tax = models.DecimalField(decimal_places=2, max_digits=11)
    total = models.DecimalField(decimal_places=2, max_digits=11)
    status = models.IntegerField(choices=STATUS)
    second_tax = models.DecimalField(decimal_places=2, max_digits=11)
    po_number = models.CharField(max_length=255, null=True)
    paid = models.DecimalField(decimal_places=2, max_digits=11, default=0)
    outstanding = models.DecimalField(
        decimal_places=2, max_digits=11, default=0)
    old_id = models.IntegerField(default=0)


class InvoiceItems(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=11)
    description = models.TextField(null=True)
    value = models.DecimalField(decimal_places=2, max_digits=11)
    name = models.CharField(max_length=255, null=True)
    item_type = models.CharField(max_length=255, null=True)

    def get_subtotal(self):
        return self.amount * self.value


class ProjectActivity(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    acitivity_type = models.CharField(max_length=255)
