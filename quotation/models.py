from django.db import models
from .choices import *
from accounts.models import Company, User
from core.models import Postcodes, Attachments
# Create your models here.


class Format(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class GSM(models.Model):
    name = models.CharField(max_length=50)
    allowed_format = models.ManyToManyField(Format)

    def __str__(self):
        return self.name


class TargetArea(models.Model):
    households = models.IntegerField()
    geo_json = models.TextField()


class Quotation(models.Model):
    # business info
    business_name = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    phone = models.CharField(max_length=50, null=True)
    postcode = models.CharField(max_length=50, null=True)
    street = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=50, null=True)

    # q_n_a
    type_of_service = models.IntegerField(choices=SERVICE_CHOICES, default=1)
    number_of_boxes = models.IntegerField(choices=BOX_TO_COLLECT, default=1)
    type_of_media = models.IntegerField(choices=TYPE_OF_MEDIA, default=1)
    require_collection = models.IntegerField(
        choices=REQUIRE_COLLECTION, default=1)

    # campaign details
    quantity_of_flyers = models.IntegerField(null=True, blank=False)
    title_of_media = models.CharField(max_length=255, null=True)
    campaign_details = models.TextField(max_length=255)
    agreed_cost = models.DecimalField(max_digits=11, decimal_places=2)
    campaign_start_date = models.DateField(null=True)
    campaign_finish_date = models.DateField(null=True)
    special_instruction = models.TextField()
    account_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        limit_choices_to={'accountant': True},
        null=True
    )

    assigned_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        limit_choices_to={'staff': True},
        null=True,
        related_name='assigned_user'
    )

    target_postcodes = models.ManyToManyField(Postcodes)

    # printing_order
    printing_required = models.BooleanField(default=False)
    pages = models.IntegerField(choices=PAGES, null=True)
    page_orientation = models.IntegerField(choices=PAGE_ORIENTATION, null=True)
    page_format = models.ForeignKey(
        Format, on_delete=models.SET_NULL, null=True)
    gsm = models.ForeignKey(GSM, on_delete=models.SET_NULL, null=True)
    colours = models.IntegerField(choices=COLORS, null=True)
    processing = models.IntegerField(choices=PROCESSING, null=True)
    attachments = models.ManyToManyField(Attachments)

    target_area = models.ForeignKey(
        TargetArea, null=True, on_delete=models.CASCADE)
    issued_date = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    old_id = models.IntegerField(default=0)

    def get_status_class(self):
        if self.status == 3:
            return 'green'
        elif self.status == 2:
            return 'yellow'
        else:
            return 'red'
