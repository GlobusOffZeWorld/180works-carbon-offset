from rest_framework import serializers, renderers
from .models import *


class stove_serializer(serializers.ModelSerializer):
    class Meta:
        model = Stove
        stoves_num = models.IntegerField()
        date = models.DateField()
        work_num = models.IntegerField()
        work_time = models.TimeField()
        fields = ('stoves_num', 'date', 'work_num', 'work_time')

class district_serializer(serializers.ModelSerializer):
    class Meta:
        model = District
        district = models.CharField(max_length=255, default=None)
        count = models.IntegerField()
        fields = ('district', 'count')
