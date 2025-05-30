from django.shortcuts import render

import joblib
import os
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TextoJuridicoSerializer
from django.conf import settings

from api.utils.transformers import AssuntosPipeline, CategoricalPipeline, MultiLabelBinarizerWrapper, StringToListTransformer

from rules.models import RegraClassificacao
from rules.utils import avaliar_expressao

# Caminho do modelo salvo
MODEL_PATH = os.path.join(settings.BASE_DIR, 'api', 'models_clf', 'stacking_clf_V2.pkl')
MODEL = joblib.load(MODEL_PATH)

class PredictSetorDestinoView(APIView):
    def post(self, request):
        message = {
            'regra': None,
            'demanda': None,
            'setor_destino': None
        }

        data = request.data

        serializer = TextoJuridicoSerializer(data=data)
        if serializer.is_valid():
            input_data = serializer.validated_data

            # Verifica as regras cadastradas.
            regras = RegraClassificacao.objects.filter(ativo=True).order_by('-prioridade')

            for regra in regras:
                try:
                    if avaliar_expressao(regra.expressao, input_data):
                        message['regra'] = regra.nome
                        message['demanda'] = regra.demanda
                        message['setor_destino'] = regra.setor_destino

                        return Response(message, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(e, status=status.HTTP_400_BAD_REQUEST)
                
                '''if verifica_regra(regra, input_data):
                    message['regra'] = regra.nome
                    message['demanda'] = regra.demanda
                    message['setor_destino'] = regra.setor_destino
                    return Response(message, status=status.HTTP_200_OK)'''

            # Cria o DataFrame para alimenta o pipeline
            #print(input_data)
            df = pd.DataFrame(input_data, index=[0])
            #print(df)
            prediction = MODEL.predict(df)
            #print(prediction)

            message['regra'] = 'Classificado por modelo de IA'
            message['setor_destino'] = prediction[0]

            return Response(message, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)