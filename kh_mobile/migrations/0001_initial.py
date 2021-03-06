# Generated by Django 4.0.3 on 2022-05-19 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bag_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255, verbose_name='Страна')),
                ('code', models.CharField(max_length=10, verbose_name='Код страны')),
                ('flag', models.ImageField(upload_to='flags', verbose_name='Флаг страны')),
            ],
            options={
                'verbose_name': 'Код страны',
                'verbose_name_plural': 'Коды стран',
            },
        ),
        migrations.CreateModel(
            name='KindLuggage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Вид багажа')),
            ],
            options={
                'verbose_name': 'Вид багажа',
                'verbose_name_plural': 'Виды багажей',
            },
        ),
        migrations.CreateModel(
            name='LSPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_storage', models.IntegerField(verbose_name='Стоимость сдачи багажа')),
                ('extension_storage', models.IntegerField(verbose_name='Стоимость хранения')),
                ('date', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Цена камеры хранения',
                'verbose_name_plural': 'Стоимость камер хранения',
            },
        ),
        migrations.CreateModel(
            name='Luggage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale', models.IntegerField(verbose_name='Баллы милиометр')),
                ('price', models.IntegerField(verbose_name='Стоимость хранения')),
                ('total_price', models.IntegerField(verbose_name='Итоговая стоимость')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Дата сдачи багажа')),
                ('ls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bag_admin.luggagestorage', verbose_name='Камера хранения')),
            ],
            options={
                'verbose_name': 'Багаж',
                'verbose_name_plural': 'Багажи',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='luggage')),
                ('luggage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kh_mobile.luggage', verbose_name='Багаж')),
            ],
            options={
                'verbose_name': 'Фотография багажа',
                'verbose_name_plural': 'Фотографии багажа',
            },
        ),
    ]
