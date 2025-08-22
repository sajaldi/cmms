# gestion_riesgos/urls.py

from django.urls import path
from .views import matriz_riesgos_view

urlpatterns = [
    path('', matriz_riesgos_view, name='matriz-riesgos'),
]