from rest_framework import serializers
from .models import *


class stove_serializer(serializers.ModelSerializer):
    class Meta:
        model = Stove
        fields = ['number', 'date', 'amount_of_stoves', 'average_number_of_hours']
