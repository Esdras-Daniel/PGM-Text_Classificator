from django.db import models

class RegraClassificacao(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    demanda = models.TextField(blank=True, null=True)
    prioridade = models.IntegerField(default=0) # Mudar para Choices
    setor_destino = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
    
class GrupoCondicao(models.Model):
    OPERADORES = [('AND', 'AND'), ('OR', 'OR')]

    regra = models.ForeignKey(
        RegraClassificacao,
        related_name='grupos',
        on_delete=models.PROTECT
    )
    operador = models.CharField(choices=OPERADORES)
    grupo_pai = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subgrupos',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'Grupo {self.pk} ({self.operador})'
    
class Condicao(models.Model):
    CAMPOS = [
        ('teor_texto', 'Teor do Texto'),
        ('classe_processo', 'Classe do Processo'),
        ('assuntos', 'Assuntos'),
        ('orgao_julgador', 'Orgão Julgador')
    ]

    OPERADORES = [
        ('CONTAINS', 'Contém'),
        ('EQUALS', 'Igual a')
    ]

    grupo = models.ForeignKey(
        GrupoCondicao,
        related_name='condicoes',
        on_delete=models.PROTECT
    )
    campo = models.CharField(
        max_length=50,
        choices=CAMPOS
    )
    operador = models.CharField(
        max_length=20,
        choices=OPERADORES
    )
    valor = models.TextField()

    def __str__(self):
        return f'{self.campo} - {self.operador} - {self.valor}'