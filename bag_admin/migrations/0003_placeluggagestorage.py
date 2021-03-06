# Generated by Django 4.0.3 on 2022-05-30 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bag_admin', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceLuggageStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=255, verbose_name='Местоположение в камере хранения')),
                ('ls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='place', to='bag_admin.luggagestorage', verbose_name='Камера хранения')),
            ],
            options={
                'verbose_name': 'Место в камере хранения',
                'verbose_name_plural': 'Места в камере хранения',
            },
        ),
    ]
