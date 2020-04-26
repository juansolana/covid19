from django.contrib import admin
from django.contrib.gis import admin
from .models import Person


class PersonAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'location', 'temperature')

admin.site.register(Person, admin.OSMGeoAdmin)