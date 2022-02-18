from django.db import models
from lostitems.models import User


# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название города")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class TimeForUnclaimed(models.Model):
    airport = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='time')
    delta_time = models.IntegerField(verbose_name="Срок хранения вещи")
    date_create = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Срок хранениея вещи в {self.airport.name} составляет {self.delta_time} суток"

    class Meta:
        verbose_name = "Время хранения вещи"
        verbose_name_plural = "Время хранения вещей"


class Airport(models.Model):
    iata = models.CharField(max_length=10, primary_key=True, unique=True, verbose_name="IATA")
    name = models.CharField(max_length=255, verbose_name="Название аэропорта")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город, в котором находится аэропорт")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Аэропорт"
        verbose_name_plural = "Аэропорты"


class LuggageStorage(models.Model):
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, verbose_name="Аэропорт")
    terminal = models.CharField(max_length=255, verbose_name="Буква терминала")
    floor = models.IntegerField(verbose_name="Этаж")
    default = models.BooleanField(default=False, verbose_name="По умолчанию")
    image = models.ImageField(upload_to='LS', verbose_name="Схема расположения камеры хранения")

    def __str__(self):
        return f"{self.airport}, Терминал {self.terminal}, Этаж {self.floor}"

    class Meta:
        verbose_name = "Камера хранения"
        verbose_name_plural = "Камеры хранения"


class WorkerInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Данные сотрудника')
    name = models.CharField(max_length=255, verbose_name="Имя и фамилия сотрудника")
    access_mobile = models.BooleanField(default=False, verbose_name="Доступ к телефону")

    def __str__(self):
        return f"Сотруднк {self.name}"

    class Meta:
        verbose_name = "Информация о сотруднике"
        verbose_name_plural = "Информация о сотрудниках"


class U_LS(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Данные сотрудника')
    ls = models.ForeignKey(LuggageStorage, on_delete=models.CASCADE, verbose_name='Камера хранения')
    date = models.DateField(verbose_name="Дата связи")

    def __str__(self):
        return f"Сотрудник {self.user} закреплен за {self.ls}"

    class Meta:
        verbose_name = "Таблица связи сотрудника и камеры хранения"
        verbose_name_plural = "Таблицы связи сотрудника и камеры хранения"


class Color(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название цвета")
    color = models.CharField(max_length=9, verbose_name="Цвет")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категории вещи")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Kind(models.Model):
    name = models.CharField(max_length=255, verbose_name="Вид вещи")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вид"
        verbose_name_plural = "Виды"


class SABItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Сотрудник САБ")
    date = models.DateTimeField(verbose_name="Дата и время находки")
    place = models.ForeignKey(LuggageStorage, on_delete=models.CASCADE, verbose_name="Место находки")
    act = models.BooleanField(default=False, verbose_name="Акт осмотра")
    comment = models.CharField(max_length=500, verbose_name="Комментарий")
    status = models.BooleanField(default=False, verbose_name="Передана на склад?")

    def __str__(self):
        return f"Вещи найденные сотрудником {self.user}"

    class Meta:
        verbose_name = "Найденные вещи сотруднком САБ"
        verbose_name_plural = "Найденные вещи сотрудником САБ"


class Photos(models.Model):
    photo = models.ImageField(upload_to='SABItem', verbose_name="Фотография")
    item = models.ForeignKey(SABItem, on_delete=models.CASCADE, related_name='photo')

    def __str__(self):
        return f"Фотография {self.item}"

    class Meta:
        verbose_name = "Фотография САБ"
        verbose_name_plural = "Фотографии САБ"


class LostItem(models.Model):
    sab_item = models.ForeignKey(SABItem, on_delete=models.CASCADE, verbose_name="Вещи найденные САБ")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Сотрудник принявший вещи")
    date = models.DateTimeField(verbose_name="Дата передачи вещей")
    comment = models.CharField(max_length=500, verbose_name="Комментарий")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, verbose_name="Цвет")
    kh = models.ForeignKey(LuggageStorage, on_delete=models.CASCADE, verbose_name="Камера хранения")
    tag = models.CharField(max_length=255, verbose_name="Номер бирки")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    kind = models.ForeignKey(Kind, on_delete=models.SET_NULL, null=True, verbose_name="Вид")
    status = models.BooleanField(default=False, verbose_name="Передана вещь")
    demanded = models.BooleanField(default=False, verbose_name="Востребована")

    def __str__(self):
        return f"Вещи {self.sab_item} переданные в {self.kh}"

    class Meta:
        verbose_name = "Вещь переданная САБ в камеру хранения"
        verbose_name_plural = "Вещи переданные САБ в камеру хранения"


class RefundItem(models.Model):
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE, verbose_name="Потерянная вещь")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Выдана сотрудником", null=True)
    fio = models.CharField(max_length=300, verbose_name="ФИО")
    series_number = models.CharField(max_length=100, verbose_name="Серия и номер")
    date_get = models.DateField(verbose_name="Дата получения")
    how_get = models.CharField(max_length=255, verbose_name="Кем выдан")
    birthday = models.DateField(verbose_name="Дата рождения")
    first_scan = models.ImageField(verbose_name="Певый скан", null=True, blank=True, upload_to=f"documents/lostitem")
    second_scan = models.ImageField(verbose_name="Второй скан", null=True, blank=True, upload_to=f"documents/lostitem")
    scan_refund = models.ImageField(verbose_name="Заявление на возврат", null=True, blank=True,
                                    upload_to=f"documents/lostitem")
    scan_receipt = models.ImageField(verbose_name="Расписка за получение", null=True, blank=True,
                                     upload_to=f"documents/lostitem")
    refund_date = models.DateTimeField(verbose_name="Дата возврата вещи")

    def __str__(self):
        return f"Возвращенне {self.lost_item}"

    class Meta:
        verbose_name = "Возвращеная вещь"
        verbose_name_plural = "Возвращенные вещи"


class RefundSAB(models.Model):
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE, verbose_name="Потерянная вещь")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Выдана сотрудником", null=True)
    close_date = models.DateField()
    broadcast_date = models.DateField()

    def __str__(self):
        return f"Возвращенне {self.lost_item}"

    class Meta:
        verbose_name = "Возвращеная вещь САБ"
        verbose_name_plural = "Возвращенные вещи САБ"


class DocScan(models.Model):
    scan = models.ImageField(verbose_name="Скан документа")
    parent = models.ForeignKey(RefundSAB, on_delete=models.CASCADE, related_name='docscan')

    def __str__(self):
        return f"Скан документа {self.parent}"

    class Meta:
        verbose_name = "Скан документа"
        verbose_name_plural = "Сканы документов"
