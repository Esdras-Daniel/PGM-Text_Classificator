from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
from .models import RegraClassificacao

'''class CondicaoInline(admin.TabularInline):
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
    list_filter = ['operador', 'regra']'''

@admin.register(RegraClassificacao)
class RegraClassificacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'setor_destino', 'prioridade', 'ativo')
    list_filter = ('ativo', 'setor_destino')
    search_fields = ('nome', 'setor_destino')
    ordering = ('prioridade',)
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget(mode='tree', height='300px')}
    }