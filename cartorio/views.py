
import requests
from django.shortcuts import render, redirect
from api.models import TextosJuridicosTreinamento
from .forms import ValidacaoForm
from django.contrib import messages

def validar_texto(request):
    if request.method == 'POST':
        form = ValidacaoForm(request.POST)
        acao = request.POST.get('acao')
        texto_id = request.POST.get('texto_id')

        try:
            texto = TextosJuridicosTreinamento.objects.get(id=texto_id)
        except TextosJuridicosTreinamento.DoesNotExist:
            messages.error(request, "Texto não encontrado.")
            return redirect('validar_texto')

        if form.is_valid():
            if acao == 'aceitar':
                # Reexecuta a previsão para garantir consistência
                dados_json = {
                    'teor_texto': texto.teor_texto,
                    'assuntos': texto.assuntos,
                    'classe_processo': texto.classe_processo,
                    'orgao_julgador': texto.orgao_julgador,
                }
                response = requests.post('http://localhost:8000/api/predict/', json=dados_json)
                setor_previsto = response.json().get('setor_destino', 'Não definido')
                texto.setor_destino_validated = setor_previsto

            elif acao == 'rejeitar':
                setor_corrigido = form.cleaned_data['setor_destino_validated']
                if not setor_corrigido:
                    messages.error(request, "Você deve informar o setor corrigido ao rejeitar uma classificação.")
                    return redirect('validar_texto')
                texto.setor_destino_validated = setor_corrigido

            texto.demanda = form.cleaned_data.get('demanda')
            texto.validated = True
            texto.save()

            messages.success(request, 'Classificação validada com sucesso!')
            return redirect('validar_texto')

        else:
            messages.error(request, 'Formulário inválido.')
            return redirect('validar_texto')

    else:
        # GET: buscar um texto aleatório não validado
        texto = TextosJuridicosTreinamento.objects.filter(validated=False).order_by('?').first()

        if not texto:
            messages.info(request, 'Não há textos pendentes de validação.')
            return render(request, 'validacao_completa.html')

        dados_json = {
            'teor_texto': texto.teor_texto,
            'assuntos': texto.assuntos,
            'classe_processo': texto.classe_processo,
            'orgao_julgador': texto.orgao_julgador,
        }
        response = requests.post('http://localhost:8000/api/predict/', json=dados_json)
        setor_previsto = response.json().get('setor_destino', 'Não definido')
        form = ValidacaoForm()

        return render(request, 'validar_texto.html', context={
            'texto': texto,
            'setor_previsto': setor_previsto,
            'form': form,
        })



'''def validar_texto(request):
    texto = TextosJuridicosTreinamento.objects.filter(validated=False).order_by('?').first()

    if not texto:
        messages.info(request, 'Não há textos pendentes de validação.')
        return render(request, 'validacao_completa.html')

    dados_json = {
        'teor_texto': texto.teor_texto,
        'assuntos': texto.assuntos,
        'classe_processo': texto.classe_processo,
        'orgao_julgador': texto.orgao_julgador,
    }

    response = requests.post('http://localhost:8000/api/predict/', json=dados_json)
    setor_previsto = response.json().get('setor_destino', 'Não definido')

    if request.method == 'POST':
        form = ValidacaoForm(request.POST)
        acao = request.POST.get('acao')
        print(acao)

        if form.is_valid():
            if acao == 'aceitar':
                texto.setor_destino_validated = setor_previsto
            elif acao == 'rejeitar':
                setor_corrigido = form.cleaned_data['setor_destino_validated']
                if not setor_corrigido:
                    messages.error(request, "Você deve informar o setor corrigido ao rejeitar uma classificação.")
                    return redirect('validar_texto')
                texto.setor_destino_validated = setor_corrigido
                
            texto.demanda = form.cleaned_data.get('demanda')
            texto.validated = True
            texto.save()

            messages.success(request, 'Classificação validada com sucesso!')
            return redirect('validar_texto')
    else:
        form = ValidacaoForm()
    
    return render(request, 'validar_texto.html', context={
        'texto': texto,
        'setor_previsto': setor_previsto,
        'form': form,
    })'''