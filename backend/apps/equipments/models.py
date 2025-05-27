from django.db import models


class Equipment(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name
