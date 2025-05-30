"""
Este código tem como objetivo inicializar o ambiente Django dentro de um Jupyter Notebook, 
para que seja possível utilizar as funcionalidades do Django como acesso ao banco de dados, 
modelos, queries, etc., fora do ambiente padrão de execução do Django (manage.py ou servidor web).

Ao chamar a função init_django(), o ambiente é configurado para permitir o uso das configurações 
do projeto Django especificado (incluindo as variáveis de ambiente e módulos necessários). 
Com isso, você consegue, por exemplo, importar seus modelos e realizar queries diretamente do Jupyter Notebook.
"""

# Importa os módulos necessários para manipular caminhos e configurações de sistema
import os, sys

# Obtém o diretório atual
PWD = os.getenv('PWD')

PROJ_MISSING_MSG = '''Set an enviroment variable:\n
"DJANGO_PROJECT=your_project_name"\n
or call:\n
"init_django(your_project_name)"
'''

# Função para inicializar o Django dentro de um ambiente externo
def init_django(project_name=None):
    # Tenta obter o nome do projeto
    project_name = project_name or os.environ.get('DJANGO_PROJECT') or None

    if project_name == None:
        raise Exception(PROJ_MISSING_MSG)
    
    # Obter o dirtório absoluto do script django_for_jupyter.py
    current_script_dir = os.path.dirname(os.path.abspath(__file__))

    # Navegar para o diretório raiz do projeto Django
    project_root = os.path.abspath(os.path.join(current_script_dir, os.pardir))
    
    # Adiciona o diretório do projeto ao inicio do sys.path para que os módulos sejam encontrados
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Define a variável de ambiente que aponta para o módulo de configurações do projeto
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')

    # Permite que chamadas assincronas sejam feitas em contextos não seguros (relevantes ao Jupyter Notebook)
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'

    # Inicializa o Django
    import django
    django.setup()

    print(f"Django initialized for project: {project_name}")
    print(f"Project root added to sys.path: {project_root}")