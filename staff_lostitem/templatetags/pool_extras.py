from django import template
from bag_admin.models import *
register = template.Library()



@register.filter(name='border')
def border(value):
    avg = 200
    col = value[1:]
    num = int(col, 16)
    r = (num >> 16) +avg
    if r > 255:
        r = 255
    elif r < 0:
        r = 0

    b = ((num >> 8) & 0x00FF) + avg
    if b > 255:
        b = 255
    elif b < 0:
        b = 0
    g = (num & 0x0000FF) + avg
    if g > 255:
        g = 255
    elif g < 0:
        g = 0
    return "#" + str(hex(g | (b << 8) | (r << 16)))[2:]


@register.filter(name='get_worker_name')
def get_worker_name(value):
    return WorkerInfo.objects.get(user=value.user).name

@register.filter(name='get_worker_name_from_user')
def get_worker_name_from_user(value):
    return WorkerInfo.objects.get(user=value).name




