from django.urls import path
from .views import validar_texto

urlpatterns = [
    path('validar/', validar_texto, name='validar_texto')
]