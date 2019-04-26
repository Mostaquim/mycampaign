
from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('',  views.Main.as_view(),name='messages'),
    path('_send', views.send_message  ,name='_send_message'),
]