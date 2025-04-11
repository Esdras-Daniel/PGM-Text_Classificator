import csv
from django.core.management.base import BaseCommand
from api.models import TextosJuridicosTreinamento

class Command(BaseCommand):
    help = 'Importa dados de treinamento de um arquivo CSV para o banco de dados.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='O caminho para o arquivo CSV.')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    TextosJuridicosTreinamento.objects.create(
                        teor_texto = row['teorTexto'],
                        assuntos = row['assuntos'],
                        classe_processo = row['classeProcesso'],
                        orgao_julgador = row['orgaoJulgador'],
                        setor_destino = row['setorDestino']
                    )
            
            self.stdout.write(self.style.SUCCESS(f'Dados importados com sucesso de "{csv_file_path}".'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Arquivo não encontrado: {csv_file_path}'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Erro na leitura do CSV: Campo: "{e}" não encontrado.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocorreu um erro durante a importação: "{e}".'))