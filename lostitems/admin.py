from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .forms import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('id', 'username', 'status')
    list_filter = ('username', 'status')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Данные пользователя', {'fields': ('email', 'phone')}),
        ('Дополнительные данные', {'fields': ('status', 'is_staff', 'is_active', 'first_join')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'phone', 'email', 'status', 'is_staff', 'is_active')}
         ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Document)
admin.site.register(VerifyCode)
admin.site.register(AddressList)
admin.site.register(Address)
admin.site.register(MileOneAir)
