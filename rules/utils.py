def avaliar_expressao(expressao, input_data):
    operador = expressao.get('operador')
    condicoes = expressao.get('condicoes', [])

    if operador == 'AND':
        return all(avaliar_condicao(cond, input_data) for cond in condicoes)
    elif operador == 'OR':
        return any(avaliar_condicao(cond, input_data) for cond in condicoes)
    else:
        raise ValueError(f"Operador Lógico inválido: {operador}")
    
def avaliar_condicao(cond, input_data):
    # Se for uma subexpressão aninhada
    if 'operador' in cond and 'condicoes' in cond:
        return avaliar_expressao(cond, input_data)
    
    campo = cond.get('campo')
    operador = cond.get('operador')
    valor = cond.get('valor')

    input_data_valor = _get_valor_campo(input_data, campo)

    if input_data_valor is None:
        return False
    
    if operador == 'equals':
        return str(input_data_valor).lower() == str(valor).lower()
    
    elif operador == 'contains':
        if isinstance(input_data_valor, list):
            return (valor in input_data_valor)
        return valor.lower() in str(input_data_valor).lower()
    
    ## Add more conditionals if needed
    else:
        raise ValueError(f"Operador inválido: {operador}")

def _get_valor_campo(obj, campo):
    if isinstance(obj, dict):
        return obj.get(campo)
    else:
        return getattr(obj, campo, None)


'''def avalia_condicao(condicao, dados):
    valor_campo = dados.get(condicao.campo)
    #print(f'Valor campo: {valor_campo}')
    #print(f'Operado: {condicao.operador}')

    if condicao.operador == 'CONTAINS':
        return condicao.valor.lower() in str(valor_campo).lower()
    if condicao.operador == 'EQUALS':
        return str(valor_campo).strip().lower() == condicao.valor.strip().lower()
    
    return False

def avalia_grupo(grupo, dados):
    resultados = []

    # Avalia condições do grupo atual
    for condicao in grupo.condicoes.all():
        #print(f'Avaliando Condição {condicao}: {avalia_condicao(condicao, dados)}')
        resultados.append(avalia_condicao(condicao, dados))

    # Avalia subgrupos recursivamente
    for subgrupo in grupo.subgrupos.all():
        #print(f'Iniciando avaliação de subgrupo: {subgrupo}')
        resultados.append(avalia_grupo(subgrupo, dados))

    if grupo.operador == 'AND':
        return all(resultados)
    elif grupo.operador == 'OR':
        return any(resultados)
    
    return False

def verifica_regra(regra, dados):
    """
    Verifica se os dados satisfazem a regra.
    'dados' é um dicionário com as chaves:
    - teor_texto
    - classe_processo
    - assuntos
    - orgao_julgador
    """

    grupo_raiz = regra.grupos.filter(grupo_pai__isnull=True).first()
    #print(f'Grupo Raiz: {grupo_raiz}')
    if not grupo_raiz:
        return False
    
    return avalia_grupo(grupo_raiz, dados)'''
