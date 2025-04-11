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

# Caminho do modelo salvo
MODEL_PATH = os.path.join(settings.BASE_DIR, 'api', 'models_clf', 'stacking_clf_V2.pkl')
MODEL = joblib.load(MODEL_PATH)

class PredictSetorDestinoView(APIView):
    def post(self, request):
        data = request.data

        # Verifica se é uma lista (múltiplas entradas)
        is_many = isinstance(data, list)

        serializer = TextoJuridicoSerializer(data=data, many=is_many)
        if serializer.is_valid():
            input_data = serializer.validated_data

            # Se for único, criamos uma lista com 1 elemento
            if not is_many:
                input_data = [input_data]

            # Cria o DataFrame para alimenta o pipeline
            df = pd.DataFrame(input_data)
            print(df)
            prediction = MODEL.predict(df)
            print(prediction)

            return Response({
                'results': [
                    {'setor_destino': p} for p in prediction
                ]
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)