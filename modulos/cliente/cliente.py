import padrao_retornos

listaClientes = []


def cadastra_cliente(nome: str, cpf: str) -> int:
    """
    cadastra um novo cliente no sistema
    retorno:
      0  - cliente criado com sucesso
      2  - cpf já existe
     -1  - parâmetros inválidos
    """

    if (not isinstance(nome, str) or nome.strip() == "" or
        not isinstance(cpf, str) or cpf.strip() == ""):
        return padrao_retornos.PARAMETRO_INVALIDO

    # verificar cpf
    for cliente in listaClientes:
        if cliente["cpf"] == cpf:
            return padrao_retornos.JA_EXISTE

    novo_cliente = {
        "id": len(listaClientes) + 1,
        "nome": nome.strip(),
        "cpf": cpf.strip(),
        "historico": []   # histórico de ingressos
    }

    listaClientes.append(novo_cliente)
    return padrao_retornos.SUCESSO


def busca_cliente(id: int) -> dict | None:
    """
    busca um cliente específico pelo ID
    retorno:
      dict(cliente) - se encontrado
      None          - se inválido ou não encontrado
    """

    if not isinstance(id, int) or id <= 0:
        return None

    for cliente in listaClientes:
        if cliente["id"] == id:
            return cliente

    return None


def lista_clientes() -> list[dict]:
    """
    lista todos os clientes cadastrados
    retorno:
      list[dict] - lista completa (possivelmente vazia)
    """
    return listaClients.copy() if (listaClients := listaClientes) else []


def remove_cliente(id: int) -> int:
    """
    remove um cliente do sistema
    retorno:
      0  - cliente removido com sucesso
      1  - cliente não encontrado
     -1  - parâmetro inválido
    """

    if not isinstance(id, int) or id <= 0:
        return padrao_retornos.PARAMETRO_INVALIDO

    for cliente in listaClientes:
        if cliente["id"] == id:
            listaClientes.remove(cliente)
            return padrao_retornos.SUCESSO

    return padrao_retornos.NAO_ENCONTRADO
