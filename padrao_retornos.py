"""
Constantes e utilitários para padronizar códigos de retorno da aplicação.
"""

# Códigos de retorno

PARAMETRO_INVALIDO = -1
SUCESSO = 0
NAO_ENCONTRADO = 1
JA_EXISTE = 2                # duplicado / já existe
CONFLITO = 3                 # conflito / regra de negócio
DEPENDENCIA_INEXISTENTE = 4  # ex.: filme_id não encontrado ao criar sessão
ERRO_SESSAO_LOTADA = 5       # sessão lotada


MENSAGENS = {
    "SUCESSO": "Sucesso",
    "PARAMETRO_INVALIDO": "Parâmetro(s) inválido(s)",
    "NAO_ENCONTRADO": "Registro não encontrado",
    "JA_EXISTE": "Registro duplicado",
    "CONFLITO": "Conflito de regra de negócio",
    "DEPENDENCIA_INEXISTENTE": "Dependência inexistente",
    "ERRO_SESSAO_LOTADA": "Sessão lotada"
}

def imprime_mensagem(codigo: int) -> str:
    """
    Retorna a mensagem associada a um código de retorno e imprime.
    """
    if codigo == PARAMETRO_INVALIDO:
        print(MENSAGENS["PARAMETRO_INVALIDO"])
        return MENSAGENS["PARAMETRO_INVALIDO"]

    elif codigo == SUCESSO:
        print(MENSAGENS["SUCESSO"])
        return MENSAGENS["SUCESSO"]

    elif codigo == NAO_ENCONTRADO:
        print(MENSAGENS["NAO_ENCONTRADO"])
        return MENSAGENS["NAO_ENCONTRADO"]

    elif codigo == JA_EXISTE:
        print(MENSAGENS["JA_EXISTE"])
        return MENSAGENS["JA_EXISTE"]

    elif codigo == CONFLITO:
        print(MENSAGENS["CONFLITO"])
        return MENSAGENS["CONFLITO"]

    elif codigo == DEPENDENCIA_INEXISTENTE:
        print(MENSAGENS["DEPENDENCIA_INEXISTENTE"])
        return MENSAGENS["DEPENDENCIA_INEXISTENTE"]

    elif codigo == ERRO_SESSAO_LOTADA:
        print(MENSAGENS["ERRO_SESSAO_LOTADA"])
        return MENSAGENS["ERRO_SESSAO_LOTADA"]

    else:
        # fallback — mas não existe no padrão oficial
        print("Erro desconhecido")
        return "Erro desconhecido"