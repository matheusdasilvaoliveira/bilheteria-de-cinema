"""
Constantes e utilitários para padronizar códigos de retorno da aplicação.
"""

# Códigos de retorno
PARAMETRO_INVALIDO = -1
SUCESSO = 0
NAO_ENCONTRADO = 1
JA_EXISTE = 2
ERRO_DESCONHECIDO = 3

# Mensagens de retorno
MENSAGENS = {
    "SUCESSO": "Sucesso",
    "PARAMETRO_INVALIDO": "Parâmetro(s) inválido(s)",
    "NAO_ENCONTRADO": "Registro não encontrado",
    "JA_EXISTE": "Registro duplicado",
    "ERRO_DESCONHECIDO": "Erro desconhecido",
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
    else:
        print(MENSAGENS["ERRO_DESCONHECIDO"])
        return MENSAGENS["ERRO_DESCONHECIDO"]