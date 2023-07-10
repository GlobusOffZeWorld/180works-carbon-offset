from django.shortcuts import render
from rest_framework.views import APIView
from .models import Stove
from .serializer import stove_serializer
from rest_framework.response import Response


class StoveView(APIView):
    def get(self, request):
        output = [
            {
                'number': output.number,
                'date': output.date,
                'amount_of_stoves': output.amount_of_stoves,
                'average_number_of_hours': output.average_number_of_hours
            } for output in Stove.objects.all()
        ]
        return Response(output)

    def post(self, request):
        serializer = stove_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
