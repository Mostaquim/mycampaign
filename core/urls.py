from django.urls import path
from .views import get_postcodes, file_upload

urlpatterns = [
    path('postcodes/', get_postcodes),
    path('files/', file_upload)
]
