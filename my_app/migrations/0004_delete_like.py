# Generated by Django 4.1.5 on 2023-03-07 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_tourrequest_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
    ]