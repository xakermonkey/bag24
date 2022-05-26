from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.


class NewUserManager(BaseUserManager):

    def create_user(self, username, password=None, status="us", is_staff=False, is_admin=False, email=None, phone=None):
        if not username:
            raise ValueError(_('The Login must be set'))
        if password == None:
            raise ValueError(_('The Password must be set'))
        user = self.model(username=username, status=status, is_staff=is_staff, is_superuser=is_admin, email=email,
                          phone=phone)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, email=None, phone=None):
        """
        Create and save a SuperUser with the given email and password.
        """
        return self.create_user(username, password, status="adm", is_staff=True, is_admin=True, email=email, phone=phone)

    def create_staff(self, username, password, email=None, phone=None):
        """
        Create and save a SuperUser with the given email and password.
        """
        return self.create_user(username, password, status="st", is_staff=True, is_admin=False, email=email, phone=phone)

    def create_administrator(self, username, password, email=None, phone=None):
        """
        Create and save a SuperUser with the given email and password.
        """
        return self.create_user(username, password, status="adm", is_staff=True, is_admin=False, email=email, phone=phone)


class User(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOISE = (
        ("us", "Пользователь"),
        ("st", "Сотрудник"),
        ("adm", "Администратор"),
    )

    phone = models.CharField(max_length=20, verbose_name="Номер телефона", null=True, blank=True)
    username = models.CharField(max_length=255, verbose_name='Логин', unique=True)
    email = models.EmailField(verbose_name="Почта", max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_join = models.BooleanField(default=True)
    verify_email = models.BooleanField(default=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOISE, default=0, verbose_name="Статус")


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = NewUserManager()

    def __str__(self):
        return self.username


    class Meta:
        verbose_name="Пользователь"
        verbose_name_plural="Пользователи"


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=500, verbose_name='Фамилия', null=True, blank=True)
    first_name = models.CharField(max_length=500, verbose_name='Имя', null=True, blank=True)
    patronymic = models.CharField(max_length=500, verbose_name='Отчество', null=True, blank=True)
    series_number = models.CharField(max_length=100, verbose_name='Серия и номер', null=True, blank=True)
    date_get = models.DateField(verbose_name='Дата выдачи', null=True, blank=True)
    how_get = models.CharField(max_length=255, verbose_name='Кем выдан', null=True, blank=True)
    birthday = models.DateField(verbose_name='День рождения', null=True, blank=True)
    first_scan = models.ImageField(verbose_name="Певый скан", upload_to=f"documents", null=True, blank=True)
    second_scan = models.ImageField(verbose_name="Второй скан", upload_to=f"documents", null=True, blank=True)
    type_doc = models.CharField(max_length=255, verbose_name="Тип документа", null=True, blank=True)
    def __str__(self):
        return "Личные данные " + self.user.username

    class Meta:
        verbose_name = "Личные данные"
        verbose_name_plural = "Личные данные"





class Address(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название адреса")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    entrance = models.IntegerField(verbose_name="Подъезд")
    floor = models.IntegerField(verbose_name="Этаж")
    apartment = models.IntegerField(verbose_name="Кватрира")
    code = models.CharField(max_length=100, verbose_name="Код домофона", null=True, blank=True)


    def __str__(self):
        return f"{self.name} адрес пользхователя {self.list_user.user.username}"

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"



class AddressList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='list_user')
    addresses = models.ManyToManyField(Address)


    def __str__(self):
        return "Список адресов" + self.user.username

    class Meta:
        verbose_name = "Список адресов"
        verbose_name_plural = "Списки адресов"


class VerifyCode(models.Model):
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    code = models.IntegerField(verbose_name="Код", null=True, blank=True)


    def __str__(self):
        return "Код верификации для " + self.phone

    class Meta:
        verbose_name = "Код верификации"
        verbose_name_plural = "Коды верификации"


class MileOneAir(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, verbose_name="Номер телефона")


    def __str__(self):
        return "Карта MileOneAir" + self.phone

    class Meta:
        verbose_name = "Карта лояльности"
        verbose_name_plural = "Карты лояльности"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)