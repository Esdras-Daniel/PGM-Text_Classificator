from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RegraClassificacao
from .utils import avaliar_expressao
from .forms import RegraClassificacaoForm
from django.db.models import Prefetch
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest
import json

class RegraCreateView(CreateView):
    model = RegraClassificacao
    form_class = RegraClassificacaoForm
    template_name = 'cadastra_regra.html'
    success_url = reverse_lazy('cadastra-regra')

    def form_valid(self, form):
        # Convertendo a expressao para dict
        try:
            expressao_raw = form.cleaned_data['expressao']
            print(type(expressao_raw), expressao_raw)

            form.instance.expressao = expressao_raw
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Expressão inválida: não é um JSON.')

        return super().form_valid(form)

    def form_invalid(self, form):
        print('Form inválido: ', form.errors)
        return super().form_invalid(form)

class TestaRegrasView(APIView):
    def post(self, request):
        dados = request.data
        regras = RegraClassificacao.objects.filter(ativo=True).order_by('-prioridade')
        #print(dados)

        for regra in regras:
            #print(regra)
            if avaliar_expressao(regra.expressao, dados):
                return Response({
                    'regra': regra.nome,
                    'setor_destino': regra.setor_destino,
                    'prioridade': regra.prioridade
                })
        
        return Response({'mensage': 'Nenhuma regra satisfeita'}, status=status.HTTP_200_OK)
