from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url

from API.views.views import GetStoveInfoView, GetDistrictInfoView
from API.views.for_front import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GetStoveInfoView.as_view(), name='on_shit'),
    path('?format=how_many_times/', get_how_many_times.as_view(), name='times'),
    path('?format=how_many_stoves/', get_how_many_stoves.as_view(), name='stoves'),
    path('?format=how_many_hours/', get_how_hours_work.as_view(), name='hours'),
    path('districts/', GetDistrictInfoView.as_view(), name='district')
]
