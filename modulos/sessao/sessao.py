from datetime import date
from modulos.filme.filme import busca_filme 
import padrao_retornos
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
nome_arquivo = 'sessoes.xml'
sessoesElement = Element('sessoes') 
comment = Comment('Dados de Sessões de Cinema')
sessoesElement.append(comment)

__all__ = [
    "cria_sessao", 
    "busca_sessao", 
    "assentos_disponiveis", 
    "reserva_assento", 
    "obtem_todas_sessoes"
]

listaSessoes = []

def formata_saida_xml(elem):
    """Formata o XML para ficar bonito (indentado)."""
    ElementTree.indent(elem, space="  ")
    return ElementTree.tostring(elem, encoding='unicode')

def grava_dados_xml():
    """Salva a estrutura atual do ElementTree no arquivo."""
    with open(nome_arquivo, 'w') as file_object:
        file_object.write(formata_saida_xml(sessoesElement))

def ler_dados_xml():
    """Lê o arquivo XML e popula a listaSessoes e o sessoesElement."""
    global listaSessoes, sessoesElement
    try:
        with open(nome_arquivo, 'rt') as f:
            tree = ElementTree.parse(f)
            root = tree.getroot()

        # Limpa a lista atual para não duplicar se chamar duas vezes
        listaSessoes.clear()

        for sessao_xml in root.findall('sessao'):
            # Reconstrói o dicionário
            dict_sessao = {
                "id": int(sessao_xml.find('id').text),
                "filme_id": int(sessao_xml.find('filme_id').text),
                "sala": int(sessao_xml.find('sala').text),
                "horario": sessao_xml.find('horario').text,
                "capacidade": int(sessao_xml.find('capacidade').text),
                "formato_exibicao": sessao_xml.find('formato_exibicao').text,
                "assentos_ocupados": []
            }
            
            # Recupera a lista de assentos ocupados
            ocupados_element = sessao_xml.find('assentos_ocupados')
            if ocupados_element:
                for assento in ocupados_element.findall('assento'):
                    dict_sessao["assentos_ocupados"].append(int(assento.text))

            listaSessoes.append(dict_sessao)

        # Atualiza a referência do Elemento Raiz para memória
        sessoesElement = root

    except FileNotFoundError:
        # Se não existe, cria a estrutura básica
        sessoesElement = Element('sessoes')
        sessoesElement.append(Comment('Dados de Sessões de Cinema'))

def obtem_todas_sessoes() -> list:
    """Retorna uma cópia da lista de todas as sessões."""
    return listaSessoes[:]

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

def _valida_horario(horario: str) -> bool:
    """
    Verifica se o horário está no formato estrito 'HH:MM'.
    Retorna True se válido, False se inválido.
    """

    if len(horario) != 5:
        return False
    
    if horario[2] != ':':
        return False

    partes = horario.split(':')
    if len(partes) != 2:
        return False
        
    hora_str, minuto_str = partes
    
    if not hora_str.isdigit() or not minuto_str.isdigit():
        return False
        

    hora = int(hora_str)
    minuto = int(minuto_str)
    
    if not (0 <= hora <= 23):
        return False
        
    if not (0 <= minuto <= 59):
        return False
        
    return True


def cria_sessao (filme_id, sala, horario, capacidade, formato_exibicao) -> int:
    

    if not filme_id or not sala or not horario or not capacidade or not formato_exibicao:
        return padrao_retornos.PARAMETRO_INVALIDO
    
    if capacidade <= 0:
        return padrao_retornos.PARAMETRO_INVALIDO
        
    if formato_exibicao not in ["dublado", "legendado"]:
        return padrao_retornos.PARAMETRO_INVALIDO
    
    if not _valida_horario(horario):
        print(f"Erro: Horário inválido (recebido: '{horario}'). Use o formato 'HH:MM'.")
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

    sessao_xml = SubElement(sessoesElement, 'sessao')
    
    SubElement(sessao_xml, 'id').text = str(nova_sessao['id'])
    SubElement(sessao_xml, 'filme_id').text = str(nova_sessao['filme_id'])
    SubElement(sessao_xml, 'sala').text = str(nova_sessao['sala'])
    SubElement(sessao_xml, 'horario').text = nova_sessao['horario']
    SubElement(sessao_xml, 'capacidade').text = str(nova_sessao['capacidade'])
    SubElement(sessao_xml, 'formato_exibicao').text = nova_sessao['formato_exibicao']
    
    # Container para assentos (vazio inicialmente)
    SubElement(sessao_xml, 'assentos_ocupados')

    grava_dados_xml()


    # Adiciona na memória
    listaSessoes.append(nova_sessao)
    
    return padrao_retornos.SUCESSO    
    # Sucesso e Persistência
    
    


def busca_sessao(sessao_id: int) -> dict | None:
    """
    Busca uma sessão específica na listaSessoes pelo seu ID.
    """
    if not isinstance(sessao_id, int) or sessao_id <= 0:
        return None
        
    for sessao in listaSessoes:
        if sessao["id"] == sessao_id:
            return sessao 
            
    return None  


def assentos_disponiveis(sessao_id:int) -> int:
    """
    Retornar a quantidade de assentos livres em uma sessão 
    """
    sessao_encontrada = busca_sessao(sessao_id)

    if sessao_encontrada is None:
        return -1
    capacidade_total = sessao_encontrada["capacidade"]
    capacidade_atual = capacidade_total - len(sessao_encontrada["assentos_ocupados"])
    return capacidade_atual 


ERRO_SESSAO_LOTADA = 5

def reserva_assento(sessao_id: int, numero_assento: int) -> int:
    """
    Reserva um assento específico em uma sessão.
    Retorna um código de status inteiro.
    """
    if not isinstance(sessao_id, int) or sessao_id <= 0:
        return padrao_retornos.PARAMETRO_INVALIDO
    
    if not isinstance(numero_assento, int) or numero_assento <= 0:
        return padrao_retornos.PARAMETRO_INVALIDO

    sessao_encontrada = busca_sessao(sessao_id)
    
    if sessao_encontrada is None:
        return padrao_retornos.NAO_ENCONTRADO 

    capacidade_total = sessao_encontrada["capacidade"]
    lista_de_ocupados = sessao_encontrada["assentos_ocupados"]

    if len(lista_de_ocupados) >= capacidade_total:
        return ERRO_SESSAO_LOTADA 

    if numero_assento > capacidade_total:
        return padrao_retornos.PARAMETRO_INVALIDO 

    
    
    if numero_assento in lista_de_ocupados:
        return padrao_retornos.JA_EXISTE 

    
    lista_de_ocupados.append(numero_assento)

    str_id = str(sessao_id)
    
    # Busca o elemento da sessão no XML
    for sess_xml in sessoesElement.findall('sessao'):
        if sess_xml.find('id').text == str_id:
            # Encontrou. Agora busca a tag de assentos
            assentos_xml = sess_xml.find('assentos_ocupados')
            
            # Adiciona o novo assento
            novo_assento_elem = SubElement(assentos_xml, 'assento')
            novo_assento_elem.text = str(numero_assento)
            
            grava_dados_xml()
            break

    
    return padrao_retornos.SUCESSO

    
def lista_sessoes(filtro_filme_id: int = None, 
                  formato_exibicao: str = None, 
                  horario_minimo: str = None) -> tuple:
    """
    Lista as sessões cadastradas com filtros opcionais.
    
    Argumentos:
        filtro_filme_id (int, opcional): ID do filme.
        formato_exibicao (str, opcional): 'dublado' ou 'legendado'.
        horario_minimo (str, opcional): Horário mínimo "HH:MM".

    Retorna uma tupla contendo: (codigo,lista)
    
    """
    
    resultado = []
    
    for sessao in listaSessoes:
        
        #Filme
        if filtro_filme_id is not None:
            if sessao["filme_id"] != filtro_filme_id:
                continue

        #Formato
        if formato_exibicao is not None:
            if sessao["formato_exibicao"] != formato_exibicao:
                continue # Pula

        #Horário Mínimo (Comparação de String "HH:MM")
        if horario_minimo is not None:
            if sessao["horario"] < horario_minimo:
                continue 

        # Se sobreviveu a todos os 'continue', adiciona na lista final
        resultado.append(sessao)

    return padrao_retornos.SUCESSO, resultado

def apaga_sessao(sessao_id: int) -> int:
    """
    Remove uma sessão do sistema, se ela não tiver ingressos vendidos.
    """

    if not isinstance(sessao_id, int) or sessao_id <= 0:
        return padrao_retornos.PARAMETRO_INVALIDO


    sessao_encontrada = busca_sessao(sessao_id)

    if sessao_encontrada is None:
        return padrao_retornos.NAO_ENCONTRADO

    if len(sessao_encontrada["assentos_ocupados"]) > 0:
        return padrao_retornos.JA_EXISTE 

    listaSessoes.remove(sessao_encontrada)
    
    str_id = str(sessao_id)
    for sess_xml in sessoesElement.findall('sessao'):
        if sess_xml.find('id').text == str_id:
            # Remove o elemento da árvore
            sessoesElement.remove(sess_xml)
            grava_dados_xml()
            break
    
    
    return padrao_retornos.SUCESSO
ler_dados_xml()