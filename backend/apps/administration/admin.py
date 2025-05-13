from django.contrib import admin

from apps.administration import models

admin.site.register(models.Faculty)
admin.site.register(models.Organization)
admin.site.register(models.Equipment)
admin.site.register(models.Location)
