# Generated by Django 2.1 on 2019-05-07 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_project_old_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='old_id',
            field=models.IntegerField(default=0),
        ),
    ]
