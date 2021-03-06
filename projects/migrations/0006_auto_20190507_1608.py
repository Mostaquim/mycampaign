# Generated by Django 2.1 on 2019-05-07 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20190507_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printingorder',
            name='priority',
            field=models.IntegerField(
                choices=[(1, 'Low'), (2, 'Normal'), (3, 'High'), (4, 'Urgent')]),
        ),
        migrations.AlterField(
            model_name='project',
            name='time_spent',
            field=models.DurationField(null=True),
        ),
    ]
