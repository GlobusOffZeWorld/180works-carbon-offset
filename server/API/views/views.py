from django.shortcuts import render
from rest_framework.views import APIView
from API.models import Stove, District
from API.serializer import stove_serializer, district_serializer
from rest_framework.response import Response


class GetStoveInfoView(APIView):
    def get(self, request):
        queryset = Stove.objects.all()
        serializer_for_queryset = stove_serializer(
            instance=queryset,
            many=True
        )
        return Response(serializer_for_queryset.data)

class GetDistrictInfoView(APIView):
    def get(self, request):
        queryset = District.objects.all()
        serializer_for_queryset = district_serializer(
            instance=queryset,
            many=True
        )
        return Response(serializer_for_queryset.data)


class DistrictView(APIView):
    def post(self, request):
        serializer = district_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class StoveView(APIView):
    def post(self, request):
        serializer = stove_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
