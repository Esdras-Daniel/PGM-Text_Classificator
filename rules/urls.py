from django.urls import path
from .views import TestaRegrasView, RegraCreateView

urlpatterns = [
    path('testa_regras/', TestaRegrasView.as_view(), name='testa-regras'),
    path('cadastra_regra/', RegraCreateView.as_view(), name='cadastra-regra')
]