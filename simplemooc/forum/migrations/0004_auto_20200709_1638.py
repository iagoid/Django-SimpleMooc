# Generated by Django 3.0.7 on 2020-07-09 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_reply_thread'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thread',
            old_name='autor',
            new_name='author',
        ),
    ]
