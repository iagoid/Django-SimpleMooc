# Generated by Django 3.0.7 on 2020-07-01 22:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0004_enrollement'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Enrollement',
            new_name='Enrollment',
        ),
    ]
