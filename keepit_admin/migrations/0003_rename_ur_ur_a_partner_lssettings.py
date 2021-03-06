# Generated by Django 4.0.3 on 2022-06-08 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bag_admin', '0005_airport_image'),
        ('keepit_admin', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ur_a',
            old_name='ur',
            new_name='partner',
        ),
        migrations.CreateModel(
            name='LSSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255, verbose_name='Токен')),
                ('token_cash_register', models.CharField(max_length=255, verbose_name='Токен кассы')),
                ('date', models.DateTimeField(auto_now=True)),
                ('ls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bag_admin.luggagestorage', verbose_name='Камера хранения')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keepit_admin.partner', verbose_name='Юридическое лицо')),
            ],
        ),
    ]
