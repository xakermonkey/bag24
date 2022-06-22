from rest_framework import serializers
from lostitems.models import *
from bag_admin.models import *


class LGSerializer(serializers.ModelSerializer):
    airport = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = LuggageStorage
        fields = "__all__"


class SABItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SABItem
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = ('item', 'photo')
