from django.contrib import admin
from .models import *


# Register your models here.


class KindAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(CodeCity)
admin.site.register(LSPrice)
admin.site.register(Luggage)
admin.site.register(PhotoLuggage)
admin.site.register(KindLuggage, KindAdmin)
