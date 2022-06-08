# Generated by Django 4.0.3 on 2022-05-19 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Automat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Состояние постамата')),
                ('token', models.CharField(max_length=255, verbose_name='Токен')),
                ('ip_cloud', models.CharField(max_length=100, verbose_name='IP подключения к облаку')),
                ('name', models.CharField(max_length=255, verbose_name='Название автомата')),
                ('urid', models.IntegerField(unique=True, verbose_name='Юридический идентификатор')),
            ],
            options={
                'verbose_name': 'Постамат',
                'verbose_name_plural': 'Постаматы',
            },
        ),
        migrations.CreateModel(
            name='Brend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название бренда')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название ячейки')),
                ('volume', models.IntegerField(verbose_name='Объем ячейки')),
                ('status', models.BooleanField(default=False, verbose_name='Состояние ячейки')),
            ],
            options={
                'verbose_name': 'Ячейка',
                'verbose_name_plural': 'Ячейки',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название компании дотавки')),
            ],
            options={
                'verbose_name': 'Компания доставки',
                'verbose_name_plural': 'Компании доставки',
            },
        ),
        migrations.CreateModel(
            name='DeliveryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=500, null=True, verbose_name='Комментарий')),
                ('create_date', models.DateField(auto_now=True, verbose_name='Дата создания заказа')),
                ('date_deliery', models.DateField(blank=True, null=True, verbose_name='ДАта отправки заказа')),
                ('date_arrival', models.DateField(blank=True, null=True, verbose_name='ДАта прибытия заказа')),
                ('track_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Трек-номер')),
                ('delivered', models.BooleanField(default=False, verbose_name='Доставлен')),
            ],
            options={
                'verbose_name': 'Вещь в дотавке',
                'verbose_name_plural': 'Вещи в доставке',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'История',
                'verbose_name_plural': 'Истории',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left_item', models.CharField(max_length=255, verbose_name='Где оставили вещь')),
                ('start_time', models.DateField(verbose_name='Дата оставление вещи')),
                ('now_item', models.CharField(max_length=255, verbose_name='Текущее местоположение вещи')),
                ('in_kh', models.BooleanField(default=False, verbose_name='В камере хранения?')),
            ],
            options={
                'verbose_name': 'Вещь',
                'verbose_name_plural': 'Вещи',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название партнера')),
                ('inn', models.CharField(max_length=100, verbose_name='ИНН')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Партнер',
                'verbose_name_plural': 'Партнеры',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='дата события')),
                ('status', models.BooleanField(default=False, verbose_name='Статус ячейки')),
            ],
            options={
                'verbose_name': 'Запись действия с ячейками',
                'verbose_name_plural': 'Записи действия с ячейками',
            },
        ),
        migrations.CreateModel(
            name='UR_A',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата связи')),
                ('automat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keepit_admin.automat', verbose_name='Постамат')),
                ('ur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keepit_admin.partner', verbose_name='Партнер')),
            ],
            options={
                'verbose_name': 'Таблица связи партнера и постамата',
                'verbose_name_plural': 'Таблицы связи партнеров и постаматов',
            },
        ),
        migrations.CreateModel(
            name='U_A',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата связи')),
                ('automat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keepit_admin.automat', verbose_name='Постамат')),
            ],
            options={
                'verbose_name': 'Таблица связи сотрудника и постамата',
                'verbose_name_plural': 'Таблицы связи сотрудников и постаматов',
            },
        ),
    ]
