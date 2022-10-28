from dataclasses import fields
from rest_framework import serializers

from logapp.models import Userdata


class Userdataserializer(serializers.ModelSerializer):
    username=serializers.CharField()
    password=serializers.CharField()
    mobile_no=serializers.IntegerField()

    class Meta:
        model=Userdata
        fields=("__all__")
