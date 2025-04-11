from django.urls import path
from .views import PredictSetorDestinoView

urlpatterns = [
    path('predict/', PredictSetorDestinoView.as_view(), name='predict-setor')
]