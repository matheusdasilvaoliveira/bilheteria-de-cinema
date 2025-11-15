from typing import Optional
from datetime import date

def criaFilme(titulo: Optional[str], sinopse: Optional[str], genero: Optional[str], duracao: Optional[float], classificacao: Optional[int], dataLancamento: Optional[str]) -> int:
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
    if (filme not in listaFilmes) and (filme["titulo"] != None):
        listaFilmes.append(filme)
        return 1
    
    return 0

listaFilmes = []