from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RegraClassificacao
from .utils import verifica_regra
from django.db.models import Prefetch

class TestaRegrasView(APIView):
    def post(self, request):
        dados = request.data
        regras = RegraClassificacao.objects.filter(ativo=True).order_by('-prioridade').prefetch_related(
            'grupos__condicoes',
            'grupos__subgrupos__condicoes'
        )
        #print(dados)

        for regra in regras:
            #print(regra)
            if verifica_regra(regra, dados):
                return Response({
                    'regra': regra.nome,
                    'setor_destino': regra.setor_destino,
                    'prioridade': regra.prioridade
                })
        
        return Response({'menagem': 'Nenhuma regra satisfeita'}, status=status.HTTP_200_OK)
