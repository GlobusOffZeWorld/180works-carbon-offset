import json

from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView

from API.models import Stove
from API.serializer import stove_serializer


class get_how_many_times(APIView):
    def how_many_times(self, request):
        queryset = Stove.objects.all()
        how_many_times = []
        for stove in queryset:
            how_many_times.append(stove['work_num'])
        serializer_for_queryset = stove_serializer(
            instance=how_many_times,
            many=True
        )
        return Response(serializer_for_queryset.data)


class get_how_many_stoves(APIView):
    def how_many_stoves(self, request):
        queryset = Stove.objects.all()
        how_many_stoves = []
        for stove in queryset:
            how_many_stoves.append(stove['stoves_num'])
        serializer_for_queryset = stove_serializer(
            instance=how_many_stoves,
            many=True
        )
        return Response(serializer_for_queryset.data)


class get_how_hours_work(APIView):
    def how_many_hours_work(self, request):
        queryset = Stove.objects.all()
        how_many_hours = []
        for stove in queryset:
            how_many_hours.append(stove['work_time'])
        serializer_for_queryset = stove_serializer(
            instance=how_many_hours,
            many=True
        )
        return Response(serializer_for_queryset.data)


def stoves_to_json(stoves):
    stoves = [model_to_dict(stoves) for stove in stoves]
    stoves_dict = {}
    for stove in stoves:
        product_id = stove['product_id']
        del stove['id']
        del stove['product_id']
        stoves_dict[product_id] = stove
    json_stoves = json.dumps(stoves_dict)
    return json_stoves
