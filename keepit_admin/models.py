from django.db import models
from lostitems.models import User, Address
from bag_admin.models import *

# Create your models here.


class Item(models.Model):
    left_item = models.CharField(max_length=255, verbose_name='Где оставили вещь')
    start_time = models.DateField(verbose_name="Дата оставление вещи")
    now_item = models.CharField(max_length=255, verbose_name="Текущее местоположение вещи")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь вещи")
    in_kh = models.BooleanField(default=False, verbose_name="В камере хранения?")

    def __str__(self):
        return f"Вещь {self.user}"

    class Meta:
        verbose_name = "Вещь"
        verbose_name_plural = "Вещи"


class Cell(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название ячейки")
    volume = models.IntegerField(verbose_name="Объем ячейки")
    status = models.BooleanField(default=False, verbose_name="Состояние ячейки")
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Вещь в ячейке")

    def __str__(self):
        return f"Ячейка {self.name}"

    class Meta:
        verbose_name = "Ячейка"
        verbose_name_plural = "Ячейки"


class Record(models.Model):
    date = models.DateField(verbose_name="дата события")
    status = models.BooleanField(default=False, verbose_name="Статус ячейки")
    operator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Кто совершил действие")
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, verbose_name="Ячейка")

    def __str__(self):
        return f"Запись в истории {self.cell.name}"

    class Meta:
        verbose_name = "Запись действия с ячейками"
        verbose_name_plural = "Записи действия с ячейками"


class History(models.Model):
    records = models.ManyToManyField(Record, verbose_name="Записи")

    def __str__(self):
        return f"История атвомата {self.automat.name}"

    class Meta:
        verbose_name = "История"
        verbose_name_plural = "Истории"


class Automat(models.Model):
    status = models.BooleanField(default=True, verbose_name="Состояние постамата")
    cells = models.ManyToManyField(Cell, verbose_name="Ячейки", related_name="automat")
    history = models.ForeignKey(History, on_delete=models.CASCADE, verbose_name="История автомата", related_name="automat")
    token = models.CharField(max_length=255,verbose_name="Токен")
    ip_cloud = models.CharField(max_length=100, verbose_name="IP подключения к облаку")
    name = models.CharField(max_length=255, verbose_name="Название автомата")
    urid = models.IntegerField(unique=True, verbose_name="Юридический идентификатор")

    def __str__(self):
        return f"Постамат {self.name}"

    class Meta:
        verbose_name = "Постамат"
        verbose_name_plural = "Постаматы"



class U_A(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    automat = models.ForeignKey(Automat, on_delete=models.CASCADE, verbose_name="Постамат")
    date = models.DateField(verbose_name="Дата связи")

    def __str__(self):
        return f"Пользователь {self.user} прикреплен к {self.automat.name}"

    class Meta:
        verbose_name = "Таблица связи сотрудника и постамата"
        verbose_name_plural = "Таблицы связи сотрудников и постаматов"


class Brend(models.Model):
    name=models.CharField(max_length=255, verbose_name="Название бренда")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Partner(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название партнера")
    inn = models.CharField(max_length=100, verbose_name="ИНН")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    brend = models.ForeignKey(Brend, on_delete=models.CASCADE, verbose_name="Бренд")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"


class UR_A(models.Model):
    automat = models.ForeignKey(Automat, on_delete=models.CASCADE, verbose_name="Постамат")
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="Партнер")
    date = models.DateField(verbose_name="Дата связи")

    def __str__(self):
        return f"Партнер {self.partner} прикреплен к {self.automat.name}"

    class Meta:
        verbose_name = "Таблица связи партнера и постамата"
        verbose_name_plural = "Таблицы связи партнеров и постаматов"


class LSSettings(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="Юридическое лицо")
    ls = models.ForeignKey(LuggageStorage, on_delete=models.CASCADE, verbose_name="Камера хранения")
    token = models.CharField(max_length=255, verbose_name="Токен")
    token_cash_register = models.CharField(max_length=255, verbose_name="Токен кассы")
    date = models.DateTimeField(auto_now=True)

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название компании дотавки")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Компания доставки"
        verbose_name_plural = "Компании доставки"


class DeliveryItem(models.Model):
    type_delibery = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компания доставки")
    comment = models.CharField(max_length=500, verbose_name="Комментарий", null=True, blank=True)
    create_date = models.DateField(verbose_name="Дата создания заказа", auto_now=True)
    date_deliery = models.DateField(verbose_name="ДАта отправки заказа", null=True, blank=True)
    date_arrival = models.DateField(verbose_name="ДАта прибытия заказа", null=True, blank=True)
    track_number = models.CharField(max_length=100, verbose_name="Трек-номер", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Адре доставки")
    delivered = models.BooleanField(default=False, verbose_name="Доставлен")
    items = models.ManyToManyField(Item, related_name='delivery_item', verbose_name="Доставляеме вещи")

    def __str__(self):
        return f"Доставка вещей пользователю {self.user}"

    class Meta:
        verbose_name = "Вещь в дотавке"
        verbose_name_plural = "Вещи в доставке"



















