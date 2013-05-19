from django.db import models
from django.contrib import admin


class WorkType(object):
    DAY = 'Day'
    NIGHT = 'Night'
    REST = 'Rest'
    OFF = 'Off'
    EXTRA = 'Extra'
    _order = [DAY, NIGHT, REST, OFF]


class WorkDay(models.Model):
    day = models.DateField()
    day_type = models.CharField(max_length=512)
    hours = models.IntegerField(null=True)
    description = models.CharField(null=True, max_length=1024)


class Holiday(models.Model):
    day = models.DateField()
    description = models.CharField(null=True, max_length=1024)

admin.site.register(Holiday)