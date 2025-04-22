from django.contrib import admin
from .models import RegraClassificacao, GrupoCondicao, Condicao

class CondicaoInline(admin.TabularInline):
    model = Condicao
    extra = 1

class GrupoCondicaoInline(admin.StackedInline):
    model = GrupoCondicao
    fk_name = 'grupo_pai'
    extra = 0
    show_change_link = True

@admin.register(GrupoCondicao)
class GrupoCondicaoAdmin(admin.ModelAdmin):
    list_display = ('regra', 'grupo_pai', 'operador')
    inlines = [CondicaoInline, GrupoCondicaoInline]
    list_filter = ['operador', 'regra']

@admin.register(RegraClassificacao)
class RegraClassificacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'setor_destino', 'prioridade', 'ativo')
    search_fields = ('nome',)
