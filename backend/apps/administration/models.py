from django.db import models


# Create your models here.


class Organization(models.Model):
    short_name = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.short_name
