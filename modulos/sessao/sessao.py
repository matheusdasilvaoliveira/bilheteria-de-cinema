from datetime import date
from modulos.filme.filme import listaFilmes
from modulos.filme.filme import busca_filme 
import padrao_retornos

listaSessoes = []

def _valida_conflito_ou_duplicata(nova_sessao: dict) -> int:
    """
    Verifica se a nova sessão conflita ou é duplicada de uma existente.
    Retorna SUCESSO (0) se for válida, ou o código de erro (JA_EXISTE).
    """
    for sessao_existente in listaSessoes:
        if (sessao_existente["filme_id"] == nova_sessao["filme_id"] and
            sessao_existente["sala"] == nova_sessao["sala"] and
            sessao_existente["horario"] == nova_sessao["horario"] and
            sessao_existente["formato_exibicao"] == nova_sessao["formato_exibicao"]):
            
            
            return padrao_retornos.JA_EXISTE 
            
        if (sessao_existente["sala"] == nova_sessao["sala"] and
            sessao_existente["horario"] == nova_sessao["horario"]):
            
            return padrao_retornos.JA_EXISTE 
            
    return padrao_retornos.SUCESSO

def cria_sessao (filme_id, sala, horario, capacidade, formato_exibicao) -> int:
    
    # Validações de Parâmetro
    if not filme_id or not sala or not horario or not capacidade or not formato_exibicao:
        return padrao_retornos.PARAMETRO_INVALIDO
    
    if capacidade <= 0:
        return padrao_retornos.PARAMETRO_INVALIDO
        
    if formato_exibicao not in ["dublado", "legendado"]:
        return padrao_retornos.PARAMETRO_INVALIDO
    
    # Validação de Filme
    filmeEncontrado = busca_filme(filme_id)
    if filmeEncontrado is None:
        return padrao_retornos.NAO_ENCONTRADO

    # Criação do Dicionário
    nova_sessao = {
        "id": len(listaSessoes) + 1,
        "filme_id": filme_id,
        "sala": sala,
        "horario": horario,
        "capacidade": capacidade,
        "formato_exibicao": formato_exibicao,
        "assentos_ocupados": []
    } 

   
    codigo_validacao = _valida_conflito_ou_duplicata(nova_sessao)
    if codigo_validacao != padrao_retornos.SUCESSO:
        return codigo_validacao
        
    # Sucesso e Persistência
    listaSessoes.append(nova_sessao)
    
    return padrao_retornos.SUCESSO
