from django.db import models

class TextosJuridicosTreinamento(models.Model):
    teor_texto = models.TextField()
    assuntos = models.CharField(max_length=255, blank=True, null=True)
    classe_processo = models.CharField(max_length=100, blank=True, null=True)
    orgao_julgador = models.CharField(max_length=200, blank=True, null=True)
    setor_destino = models.CharField(max_length=200, blank=True, null=True)
    setor_destino_validated = models.CharField(max_length=200, null=True, blank=True)
    demanda = models.TextField(null=True, blank=True)
    validated = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateField(auto_now=True, verbose_name='Atualizado em')
