# ingresso.py

from modulos.sessao.sessao import reserva_assento, busca_sessao
from modulos.cliente.cliente import busca_cliente
import padrao_retornos

listaIngressos = []


def cria_ingresso(cliente_id, sessao_id, numero_assento, preco) -> int:
    """
    Efetiva a venda de um ingresso.

    Retornos:
      0  - ingresso vendido com sucesso
      3  - assento ocupado
      1  - cliente/sessão/assento inexistentes
      5  - sessão lotada
     -1  - parâmetros inválidos
    """

    if (not isinstance(cliente_id, int) or cliente_id <= 0 or
        not isinstance(sessao_id, int) or sessao_id <= 0 or
        not isinstance(numero_assento, int) or numero_assento <= 0 or
        not isinstance(preco, (int, float)) or preco < 0):
        return padrao_retornos.PARAMETRO_INVALIDO

    cliente = busca_cliente(cliente_id)
    if cliente is None:
        return padrao_retornos.NAO_ENCONTRADO

    sessao = busca_sessao(sessao_id)
    if sessao is None:
        return padrao_retornos.NAO_ENCONTRADO

    codigo_reserva = reserva_assento(sessao_id, numero_assento)

    if codigo_reserva == padrao_retornos.SUCESSO:
        novo_ingresso = {
            "id": len(listaIngressos) + 1,
            "cliente_id": cliente_id,
            "sessao_id": sessao_id,
            "numero_assento": numero_assento,
            "preco": preco
        }
        listaIngressos.append(novo_ingresso)
        return padrao_retornos.SUCESSO

    # Tratamento dos códigos da reserva_assento
    if codigo_reserva == padrao_retornos.JA_EXISTE:
        return padrao_retornos.JA_EXISTE

    if codigo_reserva == padrao_retornos.NAO_ENCONTRADO:
        return padrao_retornos.NAO_ENCONTRADO

    if codigo_reserva == padrao_retornos.PARAMETRO_INVALIDO:
        return padrao_retornos.PARAMETRO_INVALIDO

    if codigo_reserva == 5:  # sessão lotada
        return padrao_retornos.ERRO_SESSAO_LOTADA

    # fallback
    return padrao_retornos.PARAMETRO_INVALIDO


def lista_ingressos_cliente(cliente_id: int) -> list[dict] | None:
    """
    Lista todos os ingressos de um cliente.

    Retorno:
      - list[dict]  -> se o cliente existe (com ou sem ingressos)
      - None        -> se o cliente não existe ou id inválido
    """

    if not isinstance(cliente_id, int) or cliente_id <= 0:
        return None

    cliente_encontrado = busca_cliente(cliente_id)
    if cliente_encontrado is None:
        return None

    ingressos_do_cliente = []

    for ingresso in listaIngressos:
        if ingresso["cliente_id"] == cliente_id:
            ingressos_do_cliente.append(ingresso)

    return ingressos_do_cliente

def lista_ingressos_sessao(sessao_id: int) -> list[dict]:
    """
    Lista todos os ingressos vendidos para uma sessão.

    Retorno:
      - list[dict] -> ingressos da sessão
      - []         -> sessão inexistente, id inválido, ou sem ingressos
    """

    if not isinstance(sessao_id, int) or sessao_id <= 0:
        return []

    sessao_encontrada = busca_sessao(sessao_id)
    if sessao_encontrada is None:
        return []

    ingressos_da_sessao = []

    for ingresso in listaIngressos:
        if ingresso["sessao_id"] == sessao_id:
            ingressos_da_sessao.append(ingresso)

    return ingressos_da_sessao
