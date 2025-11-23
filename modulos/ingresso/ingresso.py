# ingresso.py

from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree

from modulos.sessao.sessao import reserva_assento, busca_sessao
from modulos.cliente.cliente import busca_cliente
import padrao_retornos

# --------------------------------------------------------------------
# ESTRUTURAS GLOBAIS
# --------------------------------------------------------------------

listaIngressos = []
nome_arquivo_ingresso = "ingressos.xml"

# XML raiz
ingressosElement = Element("ingressos")
ingressosElement.append(Comment("Dados de Ingressos do Sistema"))


# --------------------------------------------------------------------
# FUNÇÕES DE XML
# --------------------------------------------------------------------

def formata_saida_xml_ingresso(elem):
    ElementTree.indent(elem, space="  ")
    return ElementTree.tostring(elem, encoding="unicode")

def grava_dados_xml_ingresso():
    """Salva o XML atual no arquivo."""
    with open(nome_arquivo_ingresso, "w") as f:
        f.write(formata_saida_xml_ingresso(ingressosElement))

def ler_dados_xml_ingresso():
    """Carrega o XML para a memória."""
    global listaIngressos, ingressosElement

    try:
        with open(nome_arquivo_ingresso, "rt") as f:
            tree = ElementTree.parse(f)
            root = tree.getroot()

        ingressosElement = root
        listaIngressos.clear()

        for ing_xml in root.findall("ingresso"):
            listaIngressos.append({
                "id": int(ing_xml.find("id").text),
                "cliente_id": int(ing_xml.find("cliente_id").text),
                "sessao_id": int(ing_xml.find("sessao_id").text),
                "numero_assento": int(ing_xml.find("numero_assento").text),
                "preco": float(ing_xml.find("preco").text)
            })

    except FileNotFoundError:
        ingressosElement = Element("ingressos")
        ingressosElement.append(Comment("Dados de Ingressos do Sistema"))


# --------------------------------------------------------------------
# FUNÇÕES PRINCIPAIS
# --------------------------------------------------------------------

def cria_ingresso(cliente_id, sessao_id, numero_assento, preco) -> int:
    """
    Efetiva a venda de um ingresso.
    Retornos:
      0  - sucesso
      3  - assento ocupado
      1  - cliente ou sessão inexistente
      5  - sessão lotada
     -1  - parâmetros inválidos
    """

    # -------------------------------------------------------------
    # 1. Validação de parâmetros
    # -------------------------------------------------------------
    if (not isinstance(cliente_id, int) or cliente_id <= 0 or
        not isinstance(sessao_id, int) or sessao_id <= 0 or
        not isinstance(numero_assento, int) or numero_assento <= 0 or
        not isinstance(preco, (int, float)) or preco < 0):
        return padrao_retornos.PARAMETRO_INVALIDO

    # -------------------------------------------------------------
    # 2. Cliente
    # -------------------------------------------------------------
    cliente = busca_cliente(cliente_id)
    if cliente is None:
        return padrao_retornos.NAO_ENCONTRADO

    # -------------------------------------------------------------
    # 3. Sessão
    # -------------------------------------------------------------
    sessao = busca_sessao(sessao_id)
    if sessao is None:
        return padrao_retornos.NAO_ENCONTRADO

    # -------------------------------------------------------------
    # 4. Reserva de assento (delegado para módulo sessão)
    # -------------------------------------------------------------
    codigo_reserva = reserva_assento(sessao_id, numero_assento)

    if codigo_reserva == padrao_retornos.SUCESSO:

        # Criar dicionário
        novo = {
            "id": len(listaIngressos) + 1,
            "cliente_id": cliente_id,
            "sessao_id": sessao_id,
            "numero_assento": numero_assento,
            "preco": preco
        }

        listaIngressos.append(novo)

        # ---------------------------------------------------------
        # Grava no XML
        # ---------------------------------------------------------
        ing_xml = SubElement(ingressosElement, "ingresso")
        SubElement(ing_xml, "id").text = str(novo["id"])
        SubElement(ing_xml, "cliente_id").text = str(novo["cliente_id"])
        SubElement(ing_xml, "sessao_id").text = str(novo["sessao_id"])
        SubElement(ing_xml, "numero_assento").text = str(novo["numero_assento"])
        SubElement(ing_xml, "preco").text = str(novo["preco"])

        grava_dados_xml_ingresso()

        return padrao_retornos.SUCESSO

    # -------------------------------------------------------------
    # TRATAMENTO DE CÓDIGOS DE ERRO DA RESERVA
    # -------------------------------------------------------------
    if codigo_reserva == padrao_retornos.JA_EXISTE:
        return padrao_retornos.JA_EXISTE

    if codigo_reserva == padrao_retornos.ERRO_SESSAO_LOTADA:
        return padrao_retornos.ERRO_SESSAO_LOTADA

    if codigo_reserva == padrao_retornos.NAO_ENCONTRADO:
        return padrao_retornos.NAO_ENCONTRADO

    if codigo_reserva == padrao_retornos.PARAMETRO_INVALIDO:
        return padrao_retornos.PARAMETRO_INVALIDO

    return padrao_retornos.PARAMETRO_INVALIDO


# --------------------------------------------------------------------
# LEITURA
# --------------------------------------------------------------------

def lista_ingressos_cliente(cliente_id: int):
    if not isinstance(cliente_id, int) or cliente_id <= 0:
        return None

    if busca_cliente(cliente_id) is None:
        return None

    return [ing for ing in listaIngressos if ing["cliente_id"] == cliente_id]


def lista_ingressos_sessao(sessao_id: int):
    if not isinstance(sessao_id, int) or sessao_id <= 0:
        return []

    if busca_sessao(sessao_id) is None:
        return []

    return [ing for ing in listaIngressos if ing["sessao_id"] == sessao_id]


def obtem_todos_ingressos():
    return listaIngressos[:]


# carregar ao importar
ler_dados_xml_ingresso()
