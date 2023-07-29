from django.shortcuts import render

from API.models import Stove


def db_info(request):
    stoves = Stove.objects.filter()
    return render(request, {'stoves': stoves})

