from django import forms
from bag_admin.models import *


class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = '__all__'


class RefoundItem(forms.ModelForm):
    class Meta:
        model = RefundItem
        exclude = ('first_scan', 'second_scan', 'scan_refund', 'scan_receipt')
