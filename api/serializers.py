from rest_framework import serializers
from .models import TextosJuridicosTreinamento

class TextoJuridicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextosJuridicosTreinamento
        fields = ['teor_texto', 'assuntos', 'classe_processo', 'orgao_julgador']