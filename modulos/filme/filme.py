from datetime import date
from typing import Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment

import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent))
import padrao_retornos

def cria_filme(titulo: str, sinopse: str, genero: str, duracao: float, classificacao: int, dataLancamento: str) -> int: 
    """
    Cria um novo filme e o adiciona à lista de filmes em cartaz se ainda não existir.
    Retorna 0 se criado com sucesso, 1 se já existir, ou -1 se algum parâmetro for inválido.
    """

    if (isinstance(titulo, str) and isinstance(sinopse, str) and isinstance(genero, str) and isinstance(duracao, float) and isinstance(classificacao, int) and (dataLancamento is None or isinstance(date.fromisoformat(dataLancamento), date))):
        tituloFormatado = titulo.strip().title()

        for filme in filmesEmCartaz:
            if filme["titulo"] == tituloFormatado:
                padrao_retornos.imprime_mensagem(padrao_retornos.JA_EXISTE)
                return padrao_retornos.JA_EXISTE
    
        id = len(filmesEmCartaz) + 1
        sinopse = sinopse.strip()
        genero = genero.strip().title()
        dataLancamento = date.fromisoformat(dataLancamento.strip()).strftime("%d/%m/%Y") if dataLancamento else ''

        filme = SubElement(filmesElement, 'filme')
        idFilme = SubElement(filme, 'id')
        idFilme.text = str(id)
        tituloFilme = SubElement(filme, 'titulo')
        tituloFilme.text = tituloFormatado
        sinopseFilme = SubElement(filme, 'sinopse')
        sinopseFilme.text = sinopse
        generoFilme = SubElement(filme, 'genero')
        generoFilme.text = genero
        duracaoFilme = SubElement(filme, 'duracao')
        duracaoFilme.text = str(duracao)
        classificacaoFilme = SubElement(filme, 'classificacao')
        classificacaoFilme.text = str(classificacao)
        dataLancamentoFilme = SubElement(filme, 'dataLancamento')
        dataLancamentoFilme.text = dataLancamento

        grava_dados_xml()

        filme = {
            "id": id,
            "titulo": tituloFormatado,
            "sinopse": sinopse,
            "genero": genero,
            "duracao": duracao,
            "classificacao": classificacao,
            "dataLancamento": dataLancamento
        }

        filmesEmCartaz.append(filme)
        padrao_retornos.imprime_mensagem(padrao_retornos.SUCESSO)
        return padrao_retornos.SUCESSO

    padrao_retornos.imprime_mensagem(padrao_retornos.PARAMETRO_INVALIDO)
    return padrao_retornos.PARAMETRO_INVALIDO

def busca_filme(filme_id: int) -> dict | None | int:
    """
    Busca um filme pelo ID.
    Retorna o dicionário do filme se encontrado, None se não encontrado, ou -1 se o parâmetro for inválido.
    """

    if (isinstance(filme_id, int)):
        for filme in filmesEmCartaz:
            if filme["id"] == filme_id:
                return filme
        return None
    else:
        return padrao_retornos.PARAMETRO_INVALIDO

def exibe_filme(filme_id: int) -> None:
    """
    Exibe os detalhes de um filme pelo ID.
    """

    filme = busca_filme(filme_id)
    if filme is None:
        print("Filme não encontrado.")
    else:
        print(f"\nId: {filme['id']}\nFilme: {filme['titulo']}\nSinopse: {filme['sinopse']}\nGênero: {filme['genero']}\nDuração: {filme['duracao']} min\nClassificação: {filme['classificacao']} anos\nData de Lançamento: {filme['dataLancamento']}")

    return None

def lista_filmes() -> list:
    return filmesEmCartaz

def exibe_filmes() -> None:
    """
    Exibe a lista de todos os filmes em cartaz.
    """

    if not filmesEmCartaz:
        print("Nenhum filme em cartaz.")
    else:
        for filme in filmesEmCartaz:
            print(f"\nId: {filme["id"]}\nFilme: {filme["titulo"]}\nSinopse: {filme["sinopse"]}\nGênero: {filme["genero"]}\nDuração: {filme["duracao"]} min\nClassificação: {filme["classificacao"]} anos\nData de Lançamento: {filme["dataLancamento"]}")

def remove_filme(filme_id: int) -> int:
    """
    Remove um filme pelo ID.
    Retorna 0 se removido com sucesso, 1 se não encontrado, ou -1 se o parâmetro for inválido.
    """

    filme = busca_filme(filme_id)

    if isinstance(filme, dict):
        filmesEmCartaz.remove(filme)

        for filmeElem in filmesElement.findall('filme'):
            idFilmeElem = filmeElem.find('id')
            if int(idFilmeElem.text) == filme_id:
                filmesElement.remove(filmeElem)
                grava_dados_xml()
                padrao_retornos.imprime_mensagem(padrao_retornos.SUCESSO)
                return padrao_retornos.SUCESSO
    elif filme is None:
        padrao_retornos.imprime_mensagem(padrao_retornos.NAO_ENCONTRADO)
        return padrao_retornos.NAO_ENCONTRADO
    else:
        padrao_retornos.imprime_mensagem(padrao_retornos.PARAMETRO_INVALIDO)
        return padrao_retornos.PARAMETRO_INVALIDO

def atualiza_dados_filme(filme_id: int, novo_titulo: Optional[str], novo_genero: Optional[str]) -> int:
    """
    Atualiza o título e/ou gênero de um filme pelo ID.
    Retorna 0 se atualizado com sucesso, 1 se não encontrado, ou -1 se o parâmetro for inválido.
    """

    if (isinstance(filme_id, int) and (isinstance(novo_titulo, str) or novo_titulo is None) and (isinstance(novo_genero, str) or novo_genero is None)):
        filme = busca_filme(filme_id)

        if isinstance(filme, dict):
            if novo_titulo is not None:
                filme["titulo"] = novo_titulo.strip().title()
            if novo_genero is not None:
                filme["genero"] = novo_genero.strip().title()

            for filmeElem in filmesElement.findall('filme'):
                idFilmeElem = filmeElem.find('id')
                if int(idFilmeElem.text) == filme_id:
                    if novo_titulo is not None:
                        tituloElem = filmeElem.find('titulo')
                        tituloElem.text = filme["titulo"]
                    if novo_genero is not None:
                        generoElem = filmeElem.find('genero')
                        generoElem.text = filme["genero"]
                    grava_dados_xml()
                    padrao_retornos.imprime_mensagem(padrao_retornos.SUCESSO)
                    return padrao_retornos.SUCESSO
        else:
            padrao_retornos.imprime_mensagem(padrao_retornos.NAO_ENCONTRADO)
            return padrao_retornos.NAO_ENCONTRADO
    else:
        padrao_retornos.imprime_mensagem(padrao_retornos.PARAMETRO_INVALIDO)
        return padrao_retornos.PARAMETRO_INVALIDO

def formata_saida_xml(elem):
    ElementTree.indent(elem, space="  ")
    return ElementTree.tostring(elem, encoding='unicode')

def grava_dados_xml():
    with open(nome_arquivo, 'w') as file_object:
        file_object.write(formata_saida_xml(filmesElement))

def ler_dados_xml():
    global filmesEmCartaz, filmesElement
    try:
        with open('filmes.xml', 'rt') as f:
            tree = ElementTree.parse(f)
            root = tree.getroot()

        for filme in root.findall('filme'):
            dictFilme = {}
            dictFilme = {
                "id": int(filme.find('id').text),
                "titulo": filme.find('titulo').text,
                "sinopse": filme.find('sinopse').text,
                "genero": filme.find('genero').text,
                "duracao": float(filme.find('duracao').text),
                "classificacao": int(filme.find('classificacao').text),
                "dataLancamento": filme.find('dataLancamento').text
            }
            filmesEmCartaz.append(dictFilme)

        # Recria o elemento raiz para futuras gravações
        filmesElement = root

    except FileNotFoundError:
        filmesElement = Element('filmes')
        comment = Comment('Dados de Filmes em Cartaz')
        filmesElement.append(comment)

filmesEmCartaz = []
nome_arquivo = 'filmes.xml'

# Persistência em arquivo xml
filmesElement = Element('filmes')
comment = Comment('Dados de Filmes em Cartaz')
filmesElement.append(comment)

# Lê dados existentes (se houver) ou cria novo arquivo
ler_dados_xml()

if __name__ == "__main__":
    # cria_filme("Interstellar", "As reservas naturais da Terra estão chegando ao fim e um grupo de astronautas recebe a missão de verificar possíveis planetas para receberem a população mundial, possibilitando a continuação da espécie. Cooper é chamado para liderar o grupo e aceita a missão sabendo que pode nunca mais ver os filhos. Ao lado de Brand, Jenkins e Doyle, ele seguirá em busca de um novo lar.", "Ficção Científica", 169.0, 10, "2014-11-06")
    # cria_filme("Toy Story", "Em um quarto de criança, os brinquedos ganham vida quando não há ninguém por perto. Woody, um boneco caubói, é o líder dos brinquedos e se sente ameaçado quando Buzz Lightyear, um moderno boneco astronauta, chega para disputar a atenção do garoto Andy. A rivalidade entre os dois brinquedos acaba levando-os a uma aventura inesperada, onde precisam aprender a trabalhar juntos para voltar para casa.", "Animação", 81.0, 0, "1995-11-22")
    # cria_filme("Matrix", "Em um futuro distópico, a humanidade vive em uma realidade simulada chamada Matrix, criada por máquinas inteligentes para subjugar os humanos enquanto suas mentes são usadas como fonte de energia. Thomas Anderson, um programador de computador que leva uma vida dupla como hacker sob o pseudônimo 'Neo', descobre a verdade sobre a Matrix e se junta a um grupo de rebeldes liderados por Morpheus para lutar contra as máquinas e libertar a humanidade.", "Ação", 136.0, 14, "1999-03-31")
    # cria_filme("Lego Movie", "Em um mundo construído inteiramente de blocos de LEGO, um personagem comum chamado Emmet é confundido com o 'Especial', o salvador profetizado que deve impedir o tirano Lord Business de destruir o universo LEGO. Juntamente com uma equipe de heróis excêntricos, Emmet embarca em uma jornada épica para salvar o mundo e descobrir seu verdadeiro potencial.", "Animação/Aventura", 100.0, 0, "2014-02-07")
    # remove_filme(2)
    # atualiza_dados_filme(1, "Interestelar", None)

    # exibe_filmes()
