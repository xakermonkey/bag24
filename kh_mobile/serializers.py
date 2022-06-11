from rest_framework import serializers
from lostitems.models import *
from bag_admin.models import *
from .models import *
from datetime import datetime, timezone
import pytz


class CityCodeSerializers(serializers.ModelSerializer):
    class Meta:
        model = CodeCity
        fields = "__all__"


class AirportSerializers(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class LuggageStorageSerializers(serializers.ModelSerializer):
    class Meta:
        model = LuggageStorage,
        fields = "__all__"


class LSInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = LuggageStorageInfo
        fields = ("location", "work_time", "conditions")


class PriceLSSerializers(serializers.ModelSerializer):
    class Meta:
        model = LSPrice
        fields = "__all__"


class KindLuggageSerializers(serializers.ModelSerializer):
    class Meta:
        model = KindLuggage
        fields = "__all__"


class PhotoLuggageSerializers(serializers.ModelSerializer):
    class Meta:
        model = PhotoLuggage
        fields = ("photo",)


class LuggageSerializers(serializers.ModelSerializer):
    photo = PhotoLuggageSerializers(many=True, read_only=True)
    kind_luggage = serializers.SlugRelatedField(slug_field="name", read_only=True)
    len_day = serializers.SerializerMethodField()

    class Meta:
        model = Luggage
        fields = "__all__"

    def get_len_day(self, obj):
        local_time = obj.date_send.replace(tzinfo=timezone.utc).astimezone(tz=pytz.timezone("Europe/Moscow"))
        now = datetime.now(tz=pytz.timezone("Europe/Moscow"))
        length = now - local_time
        return length.days


class DocumentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"

# class CreditCardSerializers(serializers.ModelSerializer):
#     class Meta:
#         model=CreditCard
#         fields="__all__"


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "verify_email", "email", "phone")
