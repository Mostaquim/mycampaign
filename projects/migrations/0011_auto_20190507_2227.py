# Generated by Django 2.1 on 2019-05-07 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_invoice_old_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='currency',
            field=models.IntegerField(choices=[(1, '£')], default=1),
        ),
    ]
