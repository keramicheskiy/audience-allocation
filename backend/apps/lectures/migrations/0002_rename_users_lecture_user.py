# Generated by Django 5.2.1 on 2025-05-27 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lecture',
            old_name='users',
            new_name='user',
        ),
    ]
