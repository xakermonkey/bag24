# Generated by Django 4.0.3 on 2022-06-08 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kh_mobile', '0009_codecity_iso2_codecity_iso3'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codecity',
            name='iso2',
        ),
        migrations.RemoveField(
            model_name='codecity',
            name='iso3',
        ),
    ]
