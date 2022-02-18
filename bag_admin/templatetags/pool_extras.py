from django import template
from bag_admin.models import *
register = template.Library()



@register.filter(name='get_airport')
def get_airport(value):
    ls = U_LS.objects.filter(user=value.user).first().ls
    return f"{ls.airport}. Терминал {ls.terminal}"\


@register.filter(name='get_things')
def get_things(value):
    return SABItem.objects.filter(user=value.user).count() + LostItem.objects.filter(user=value.user).count()

@register.filter(name='get_staff')
def get_staff(value):
    u_ls = U_LS.objects.filter(ls__airport=value)
    arr = []
    for i in u_ls:
        if not i.user in arr:
            arr.append(i.user)
    return len(arr)


@register.filter(name='get_airport_things')
def get_airport_things(value):
    u_ls = U_LS.objects.filter(ls__airport=value)
    arr = []
    sum = 0
    for i in u_ls:
        if not i.user in arr:
            arr.append(i.user)
            sum += SABItem.objects.filter(user=i.user).count() + LostItem.objects.filter(user=i.user).count()
    return sum





