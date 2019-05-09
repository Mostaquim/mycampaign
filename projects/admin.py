from django.contrib import admin
from .models import Project, PrintingOrder, Invoice, InvoiceItems
# Register your models here.

admin.site.register(Project)
admin.site.register(PrintingOrder)
admin.site.register(Invoice)
admin.site.register(InvoiceItems)
