# Generated by Django 2.1 on 2019-05-07 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_invoice_po_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='outstanding',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11),
        ),
        migrations.AddField(
            model_name='invoice',
            name='paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11),
        ),
    ]