from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url
from API.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', StoveView.as_view(), name='on_shit')
]
