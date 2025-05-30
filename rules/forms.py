from django import forms
from .models import RegraClassificacao

SETOR_CHOICES = [
    ('', '--- Selecione um Setor Destino ---'),
    ("Fiscal", "Fiscal"),
    ("Administrativa", "Administrativa"),
    ("Contabilidade", "Contabilidade"),
    ("Judicial", "Judicial"),
    ("Saúde", "Saúde"),
    ("Meio Ambiente", "Meio Ambiente"),
    ("Patrimonial", "Patrimonial"),
]

class RegraClassificacaoForm(forms.ModelForm):
    setor_destino = forms.ChoiceField(
        choices=SETOR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Setor de Destino'
    )

    class Meta:
        model = RegraClassificacao
        fields = ['nome', 'descricao', 'demanda', 'prioridade', 'setor_destino', 'expressao']
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '100',
                'placeholder': 'Breve descrição'
            }),
            'demanda': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descreva a demanda'
            }),
            'expressao': forms.HiddenInput()
        }

    def clean_expressao(self):
        data = self.cleaned_data['expressao']
        if not isinstance(data, dict):
            raise forms.ValidationError('A expressão deve ser um JSON válido.')
        if 'operador' not in data or 'condicoes' not in data:
            raise forms.ValidationError('Expressão incompleta: faltam operador ou condições.')
        return data