from django import forms

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

class ValidacaoForm(forms.Form):
    setor_destino_validated = forms.ChoiceField(
        choices=SETOR_CHOICES,
        required=False,
        label="Setor Destino Corrigido",
    )
    demanda = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}), 
        required=False,
        label="Demanda (opcional)",
    )

    def clean(self):
        cleaned_data = super().clean()

        if self.data.get('acao') == 'rejeitar' and not cleaned_data.get('setor_destino_validated'):
            raise forms.ValidationError("Você deve preencher o setor destino validado ao rejeitar a classificação.")

        return cleaned_data