from django.urls import path
from .views import TestaRegrasView

urlpatterns = [
    path('testa-regras/', TestaRegrasView.as_view(), name='teste-regras')
]