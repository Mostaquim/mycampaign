# Generated by Django 2.1 on 2019-05-06 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.IntegerField(choices=[(1, '&#163;')])),
                ('sent_date', models.DateField(auto_now_add=True)),
                ('issue_date', models.DateField()),
                ('due_date', models.DateField()),
                ('paid_date', models.DateField(null=True)),
                ('terms', models.TextField()),
                ('discount', models.DecimalField(decimal_places=2, max_digits=11)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=11)),
                ('total', models.DecimalField(decimal_places=2, max_digits=11)),
                ('status', models.IntegerField(choices=[(1, 'Sent'), (2, 'Open'), (3, 'Paid'), (4, 'Partially paid'), (5, 'Cancelled')])),
                ('second_tax', models.DecimalField(decimal_places=2, max_digits=11)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=11)),
                ('description', models.TextField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=11)),
                ('name', models.CharField(max_length=255, null=True)),
                ('item_type', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrintingOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pages', models.IntegerField(choices=[(1, 'Single Sided'), (2, 'Double Sided'), (3, '2 Pages'), (4, '4 Pages'), (5, '6 Pages'), (6, '8 Pages'), (7, '10 Pages'), (8, '12 Pages')])),
                ('page_orientation', models.IntegerField(choices=[(1, 'Portrait'), (2, 'Landscape')])),
                ('colours', models.IntegerField(choices=[(1, '1/0-coloured Black'), (2, '2/0-coloured Black + Pantone'), (3, '2/0-coloured Black + Gold'), (4, '4/0-coloured CMYK')])),
                ('processing', models.IntegerField(choices=[(1, 'Trimming'), (2, 'Trimming Corner Rounded')])),
                ('priority', models.IntegerField(choices=[(1, 'Low'), (2, 'Normal'), (3, 'High'), (4, 'Urgent')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_service', models.IntegerField(choices=[(1, 'Business To Business'), (2, 'Hand To Hand'), (3, 'Direct Mail'), (4, 'Residential Homes'), (5, 'Shared Distribution'), (6, 'Consultation Distribution')], default=1)),
                ('number_of_boxes', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4 or more'), (5, 'N/A')], default=1)),
                ('type_of_media', models.IntegerField(choices=[(1, 'Flyer'), (2, 'Leaflet'), (3, 'Folded Leaflet'), (4, 'Other')], default=1)),
                ('require_collection', models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], default=1)),
                ('quantity_of_flyers', models.IntegerField(null=True)),
                ('title_of_media', models.CharField(max_length=255, null=True)),
                ('campaign_details', models.TextField(max_length=255)),
                ('agreed_cost', models.DecimalField(decimal_places=2, max_digits=11)),
                ('campaign_start_date', models.DateField()),
                ('campaign_finish_date', models.DateField()),
                ('special_instruction', models.TextField()),
                ('progress', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('attachments', models.ManyToManyField(to='core.Attachments')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company', to='accounts.Company')),
                ('project_admin', models.ForeignKey(limit_choices_to={'staff': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('acitivity_type', models.CharField(max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
