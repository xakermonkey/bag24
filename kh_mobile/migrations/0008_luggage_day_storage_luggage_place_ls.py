# Generated by Django 4.0.3 on 2022-05-30 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bag_admin', '0003_placeluggagestorage'),
        ('kh_mobile', '0007_luggage_issued_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='luggage',
            name='day_storage',
            field=models.IntegerField(default=0, verbose_name='Время хранения багажа'),
        ),
        migrations.AddField(
            model_name='luggage',
            name='place_ls',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bag_admin.placeluggagestorage', verbose_name='Местоположение в камере хранения'),
        ),
    ]