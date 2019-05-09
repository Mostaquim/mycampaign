# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Clients(models.Model):
    company_id = models.IntegerField(blank=True, null=True)
    firstname = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=180, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    mobile = models.CharField(max_length=25, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    zipcode = models.CharField(max_length=30)
    userpic = models.CharField(max_length=150)
    city = models.CharField(max_length=45, blank=True, null=True)
    hashed_password = models.CharField(max_length=255, blank=True, null=True)
    inactive = models.IntegerField(blank=True, null=True)
    access = models.CharField(max_length=150, blank=True, null=True)
    last_active = models.CharField(max_length=50, blank=True, null=True)
    last_login = models.CharField(max_length=50, blank=True, null=True)
    twitter = models.CharField(max_length=255)
    skype = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)
    googleplus = models.CharField(max_length=255)
    youtube = models.CharField(max_length=255)
    pinterest = models.CharField(max_length=255)
    token = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    signature = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients'


class Companies(models.Model):
    reference = models.IntegerField()
    name = models.CharField(max_length=140, blank=True, null=True)
    client_id = models.CharField(max_length=140, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    mobile = models.CharField(max_length=25, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    zipcode = models.CharField(max_length=30)
    city = models.CharField(max_length=45, blank=True, null=True)
    inactive = models.IntegerField(blank=True, null=True)
    website = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    vat = models.CharField(max_length=250, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255)
    skype = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)
    googleplus = models.CharField(max_length=255)
    youtube = models.CharField(max_length=255)
    pinterest = models.CharField(max_length=255)
    terms = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'companies'


class CompanyHasAdmins(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_id = models.BigIntegerField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    access = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_has_admins'


class InvoiceHasItems(models.Model):
    invoice_id = models.IntegerField()
    item_id = models.IntegerField()
    amount = models.CharField(max_length=11, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    task_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'invoice_has_items'


class InvoiceHasPayments(models.Model):
    id = models.BigAutoField(primary_key=True)
    invoice_id = models.BigIntegerField(blank=True, null=True)
    reference = models.CharField(max_length=250, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    date = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    notes = models.TextField()
    user_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice_has_payments'


class Invoices(models.Model):
    reference = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField()
    status = models.CharField(max_length=50, blank=True, null=True)
    currency = models.CharField(max_length=20, blank=True, null=True)
    issue_date = models.CharField(max_length=20, blank=True, null=True)
    due_date = models.CharField(max_length=20, blank=True, null=True)
    sent_date = models.CharField(max_length=20, blank=True, null=True)
    paid_date = models.CharField(max_length=20, blank=True, null=True)
    terms = models.TextField(blank=True, null=True)
    discount = models.CharField(max_length=50, blank=True, null=True)
    subscription_id = models.CharField(max_length=50, blank=True, null=True)
    project_id = models.IntegerField(blank=True, null=True)
    tax = models.CharField(max_length=255, blank=True, null=True)
    estimate = models.IntegerField(blank=True, null=True)
    estimate_status = models.CharField(max_length=255, blank=True, null=True)
    estimate_accepted_date = models.CharField(
        max_length=255, blank=True, null=True)
    estimate_sent = models.CharField(max_length=255, blank=True, null=True)
    sum = models.FloatField(blank=True, null=True)
    second_tax = models.CharField(max_length=5, blank=True, null=True)
    estimate_reference = models.CharField(
        max_length=255, blank=True, null=True)
    po_number = models.CharField(max_length=255)
    paid = models.FloatField(blank=True, null=True)
    outstanding = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoices'


class Printorders(models.Model):
    project_id = models.IntegerField()
    size = models.CharField(max_length=10)
    gsm = models.CharField(max_length=20)
    qty = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    reference = models.IntegerField()
    company_id = models.IntegerField()
    invoice_id = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    issue_date = models.CharField(max_length=20)
    ip = models.CharField(max_length=200)
    orien = models.CharField(max_length=70)
    color = models.CharField(max_length=70)
    proc = models.CharField(max_length=70)
    pages = models.CharField(max_length=70)
    files = models.TextField()

    class Meta:
        managed = False
        db_table = 'printorders'


class Privatemessages(models.Model):
    status = models.CharField(max_length=150)
    sender = models.CharField(max_length=250)
    recipient = models.CharField(max_length=250)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    time = models.CharField(max_length=100)
    conversation = models.CharField(max_length=32, blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)
    attachment = models.CharField(max_length=255, blank=True, null=True)
    attachment_link = models.CharField(max_length=255, blank=True, null=True)
    receiver_delete = models.IntegerField(blank=True, null=True)
    marked = models.IntegerField(blank=True, null=True)
    read = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'privatemessages'


class ProjectHasActivities(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_id = models.BigIntegerField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    client_id = models.BigIntegerField(blank=True, null=True)
    datetime = models.CharField(max_length=250, blank=True, null=True)
    subject = models.CharField(max_length=250, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_has_activities'


class ProjectHasFiles(models.Model):
    project_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    client_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=80, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    filename = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    savename = models.CharField(max_length=200, blank=True, null=True)
    phase = models.CharField(max_length=100, blank=True, null=True)
    date = models.CharField(max_length=50, blank=True, null=True)
    download_counter = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_has_files'


class ProjectHasInvoices(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_id = models.BigIntegerField(blank=True, null=True)
    invoice_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_has_invoices'


class ProjectHasMilestones(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    due_date = models.CharField(max_length=250, blank=True, null=True)
    start_date = models.CharField(max_length=250, blank=True, null=True)
    orderindex = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_has_milestones'


class ProjectHasTasks(models.Model):
    project_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    public = models.IntegerField(blank=True, null=True)
    datetime = models.IntegerField(blank=True, null=True)
    due_date = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    pstatus = models.CharField(max_length=50)
    client_id = models.IntegerField(blank=True, null=True)
    created_by_client = models.IntegerField(blank=True, null=True)
    tracking = models.IntegerField(blank=True, null=True)
    time_spent = models.IntegerField(blank=True, null=True)
    milestone_id = models.IntegerField(blank=True, null=True)
    invoice_id = models.IntegerField(blank=True, null=True)
    milestone_order = models.IntegerField(blank=True, null=True)
    task_order = models.IntegerField(blank=True, null=True)
    progress = models.IntegerField(blank=True, null=True)
    start_date = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_has_tasks'


class ProjectHasTimesheets(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    client_id = models.IntegerField(blank=True, null=True)
    task_id = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=250, blank=True, null=True)
    start = models.CharField(max_length=250, blank=True, null=True)
    end = models.CharField(max_length=250, blank=True, null=True)
    invoice_id = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_has_timesheets'


class ProjectHasWorkers(models.Model):
    project_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_has_workers'


class Projects(models.Model):
    reference = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start = models.CharField(max_length=20, blank=True, null=True)
    end = models.CharField(max_length=20, blank=True, null=True)
    notifiction_deadline = models.IntegerField()
    progress = models.DecimalField(
        max_digits=3, decimal_places=0, blank=True, null=True)
    phases = models.CharField(max_length=150, blank=True, null=True)
    tracking = models.IntegerField(blank=True, null=True)
    time_spent = models.IntegerField(blank=True, null=True)
    datetime = models.IntegerField(blank=True, null=True)
    sticky = models.CharField(max_length=1, blank=True, null=True)
    category = models.CharField(max_length=150, blank=True, null=True)
    company_id = models.IntegerField()
    note = models.TextField()
    progress_calc = models.IntegerField(blank=True, null=True)
    postcodes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    anomr = models.CharField(max_length=255)
    hide_tasks = models.IntegerField(blank=True, null=True)
    enable_client_tasks = models.IntegerField(blank=True, null=True)
    gc_event_id = models.IntegerField()
    area = models.TextField()

    class Meta:
        managed = False
        db_table = 'projects'


class Quotations(models.Model):
    # type of service
    # 1, 2 ,4 ,5 ,6, 7
    q1 = models.CharField(max_length=50, blank=True, null=True)
    # type of media
    q2 = models.CharField(max_length=50, blank=True, null=True)
    # require collection
    q3 = models.CharField(max_length=50, blank=True, null=True)
    # quantity of flyers
    q4 = models.CharField(max_length=150, blank=True, null=True)
    # detail about campaign
    q5 = models.TextField(blank=True, null=True)
    # number of boxes
    q6 = models.CharField(max_length=50, blank=True, null=True)

    company = models.CharField(max_length=150, blank=True, null=True)
    fullname = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    zip = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    target_postcodes = models.TextField(
        db_column='Target_PostCodes', blank=True, null=True)
    ip = models.TextField()
    start = models.CharField(max_length=255)
    cost = models.TextField(blank=True, null=True)
    date = models.CharField(max_length=50, blank=True, null=True)
    created = models.IntegerField()
    status = models.CharField(max_length=150, blank=True, null=True)
    media_title = models.CharField(max_length=110)
    uploads = models.TextField()
    uploader_count = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    replied = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=255)
    vat = models.CharField(max_length=255)
    # Field name made lowercase.
    target_area = models.TextField(db_column='Target_Area')
    refer = models.CharField(max_length=25, blank=True, null=True)

    pages = models.CharField(max_length=150)
    page_orien = models.CharField(max_length=150)
    page_format = models.CharField(max_length=150)
    page_paper = models.CharField(max_length=150)
    page_color = models.CharField(max_length=150)
    page_proc = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'quotations'


class Users(models.Model):
    username = models.CharField(max_length=45, blank=True, null=True)
    firstname = models.CharField(max_length=120, blank=True, null=True)
    lastname = models.CharField(max_length=120, blank=True, null=True)
    hashed_password = models.CharField(max_length=128, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    status = models.CharField(max_length=8, blank=True, null=True)
    admin = models.CharField(max_length=1, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    userpic = models.CharField(max_length=250, blank=True, null=True)
    title = models.CharField(max_length=150)
    access = models.CharField(max_length=150)
    last_active = models.CharField(max_length=50, blank=True, null=True)
    last_login = models.CharField(max_length=50, blank=True, null=True)
    queue = models.BigIntegerField(blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    signature = models.TextField(blank=True, null=True)
    account = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'users'
