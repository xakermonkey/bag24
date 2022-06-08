from django.db import models
from lostitems.models import *
from bag_admin.models import *


# Create your models here.


class CodeCity(models.Model):
    city = models.CharField(max_length=255, verbose_name="Страна")
    code = models.CharField(max_length=10, verbose_name="Код страны")
    flag = models.ImageField(upload_to="flags", verbose_name="Флаг страны")
    # iso3 = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        verbose_name = "Код страны"
        verbose_name_plural = "Коды стран"

    def __str__(self):
        return f"{self.city} {self.code}"


class LSPrice(models.Model):
    ls = models.ForeignKey(LuggageStorage, on_delete=models.CASCADE, verbose_name="Камера хранения")
    price_storage = models.IntegerField(verbose_name="Стоимость сдачи багажа")
    extension_storage = models.IntegerField(verbose_name="Стоимость хранения")
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Цена камеры хранения"
        verbose_name_plural = "Стоимость камер хранения"

    def __str__(self):
        return f"Стоимость  {self.ls}"


class KindLuggage(models.Model):
    name = models.CharField(max_length=255, verbose_name="Вид багажа")

    class Meta:
        verbose_name = "Вид багажа"
        verbose_name_plural = "Виды багажей"

    def __str__(self):
        return self.name


class Luggage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    ls = models.ForeignKey(LuggageStorage, on_delete=models.CASCADE, verbose_name="Камера хранения")
    kind_luggage = models.ForeignKey(KindLuggage, on_delete=models.SET_NULL, null=True, verbose_name="Вид вещи")
    sale_storage = models.IntegerField(verbose_name="Количество списанных баллов mileonair за сдачу багажа")
    sale_day_storage = models.IntegerField(verbose_name="Количество списанных баллов mileonair за хранение багажа",
                                           null=True, blank=True)
    price_storage = models.IntegerField(verbose_name="Стоимость сдачи")
    price_per_day = models.IntegerField(verbose_name="Стоимость 1 дня хранения")
    price_day_storage = models.IntegerField(verbose_name="Стоимость хранения", null=True, blank=True)
    total_price = models.IntegerField(verbose_name="Итоговая стоимость", null=True, blank=True)
    date_create = models.DateTimeField(verbose_name="Дата создания багажа")
    date_send = models.DateTimeField(null=True, blank=True, verbose_name="Дата сдачи багажа")
    date_take = models.DateTimeField(null=True, blank=True, verbose_name="Дата получения багажа")
    issued_staff = models.BooleanField(default=False, verbose_name="Оформлено сотрудником")
    day_storage = models.IntegerField(verbose_name="Время хранения багажа", default=0)
    place_ls = models.ForeignKey(PlaceLuggageStorage, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="Местоположение в камере хранения")

    class Meta:
        verbose_name = "Багаж"
        verbose_name_plural = "Багажи"

    def __str__(self):
        return f"Багаж {self.user} сданный в {self.ls}  в {self.date_send}"


class PhotoLuggage(models.Model):
    luggage = models.ForeignKey(Luggage, on_delete=models.CASCADE, verbose_name="Багаж", related_name="photo")
    photo = models.ImageField(upload_to="luggage")

    class Meta:
        verbose_name = "Фотография багажа"
        verbose_name_plural = "Фотографии багажа"

    def __str__(self):
        return f"Фотографии {self.luggage}"
