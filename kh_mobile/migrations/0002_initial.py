# Generated by Django 4.0.3 on 2022-05-19 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bag_admin', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kh_mobile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='luggage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='lsprice',
            name='ls',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bag_admin.luggagestorage', verbose_name='Камера хранения'),
        ),
    ]
