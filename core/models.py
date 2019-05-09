from django.db import models

# Create your models here.


class Postcodes(models.Model):
    full_name = models.CharField(max_length=13)
    area = models.CharField(max_length=2)
    district = models.CharField(max_length=2)
    sector = models.CharField(max_length=1)
    # Field name made lowercase.
    locality = models.CharField(db_column='Locality', max_length=64)
    # Field name made lowercase.
    residential = models.CharField(db_column='Residential', max_length=11)
    # Field name made lowercase.
    business = models.CharField(db_column='Business', max_length=8)
    # Field name made lowercase.
    total = models.CharField(db_column='Total', max_length=9)

    def __str__(self):
        return self.full_name

    class Meta:
        managed = False
        db_table = 'postcodes'


class Attachments(models.Model):
    name = models.CharField(max_length=255)
    attachment = models.FileField()
