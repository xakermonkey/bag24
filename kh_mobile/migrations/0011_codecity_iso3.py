# Generated by Django 4.0.3 on 2022-06-08 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kh_mobile', '0010_remove_codecity_iso2_remove_codecity_iso3'),
    ]

    operations = [
        migrations.AddField(
            model_name='codecity',
            name='iso3',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]