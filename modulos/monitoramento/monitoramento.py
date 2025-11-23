from modulos.filme.filme import busca_filme
from modulos.sessao.sessao import busca_sessao
from modulos.ingresso.ingresso import listaIngressos, lista_ingressos_sessao


# ---------------------------------------------------------
# (19) receita_e_ingressos(filme_id)
# ---------------------------------------------------------
def receita_e_ingressos(filme_id: int):
    """Retorna receita total e ingressos vendidos de um filme."""

    if not isinstance(filme_id, int) or filme_id <= 0:
        return None

    filme = busca_filme(filme_id)
    if filme is None:
        return None

    total_receita = 0.0
    total_ingressos = 0

    # percorre todos os ingressos existentes
    for ingresso in listaIngressos:
        sessao = busca_sessao(ingresso["sessao_id"])
        if sessao and sessao["filme_id"] == filme_id:
            total_ingressos += 1
            total_receita += ingresso["preco"]

    if total_ingressos == 0:
        return None

    return {
        "receita": total_receita,
        "ingressos_vendidos": total_ingressos
    }


# ---------------------------------------------------------
# (20) filme_mais_assistido(lista_sessoes)
# ---------------------------------------------------------
def filme_mais_assistido(sessoes: list):
    """Retorna o filme mais assistido considerando uma lista de sessões."""

    if not sessoes or not isinstance(sessoes, list):
        return None

    quantidade_por_filme = {}   # filme_id -> quantidade

    for sessao in sessoes:
        qtd = len(lista_ingressos_sessao(sessao["id"]))
        filme_id = sessao["filme_id"]

        if filme_id not in quantidade_por_filme:
            quantidade_por_filme[filme_id] = 0

        quantidade_por_filme[filme_id] += qtd

    if not quantidade_por_filme:
        return None

    # achar o filme com maior número de ingressos
    filme_mais = max(quantidade_por_filme, key=lambda f: quantidade_por_filme[f])
    qtd_max = quantidade_por_filme[filme_mais]

    filme_dict = busca_filme(filme_mais)
    if not filme_dict:
        return None

    return {
        "titulo_filme": filme_dict["titulo"],
        "quantidade_ingressos": qtd_max
    }


# ---------------------------------------------------------
# (21) receita_e_ocupacao_sessao(sessao_id)
# ---------------------------------------------------------
def receita_e_ocupacao_sessao(sessao_id: int):
    """Retorna receita e porcentagem de ocupação da sessão."""

    if not isinstance(sessao_id, int) or sessao_id <= 0:
        return None

    sessao = busca_sessao(sessao_id)
    if sessao is None:
        return None

    ingressos = lista_ingressos_sessao(sessao_id)
    capacidade = sessao["capacidade"]

    qtd = len(ingressos)
    receita = sum(i["preco"] for i in ingressos)

    ocupacao = (qtd / capacidade) * 100 if capacidade > 0 else 0.0

    return {
        "receita": float(receita),
        "ocupacao_porcentagem": ocupacao
    }


# ---------------------------------------------------------
# (22) conta_ingressos(lista_sessoes)
# ---------------------------------------------------------
def conta_ingressos(sessoes: list):
    """Conta ingressos vendidos em todas as sessões informadas."""

    if sessoes is None:
        return None

    if not isinstance(sessoes, list):
        return -1

    total = 0
    for sessao in sessoes:
        ingressos = lista_ingressos_sessao(sessao["id"])
        total += len(ingressos)

    return total

