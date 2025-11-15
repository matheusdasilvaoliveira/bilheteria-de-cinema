from typing import Optional
from datetime import date
import padrao_retornos

def criaFilme(titulo: str, sinopse: str, genero: str, duracao: float, classificacao: int, dataLancamento: str) -> int:
    """
    Cria um novo filme e o adiciona à lista de filmes se ainda não existir.
    """

    filme = {
        "id": len(listaFilmes) + 1,
        "titulo": titulo,
        "sinopse": sinopse,
        "genero": genero,
        "duracao": duracao,
        "classificacao": classificacao,
        "dataLancamento": date.fromisoformat(dataLancamento) if dataLancamento else None
    }

    print(f"filme = {filme}")

    if filme in listaFilmes:
        return padrao_retornos.imprime_mensagem(padrao_retornos.MENSAGENS.JA_EXISTE)
    else:
        listaFilmes.append(filme)
        return padrao_retornos.imprime_mensagem(padrao_retornos.MENSAGENS.SUCESSO)

    return padrao_retornos.imprime_mensagem(padrao_retornos.MENSAGENS.PARAMETRO_INVALIDO)

listaFilmes = []