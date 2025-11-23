import padrao_retornos
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment

nome_arquivo = 'clientes.xml'
clientesElement = Element('clientes')
comment = Comment('Dados de Clientes')
clientesElement.append(comment)

listaClientes = []


def formata_saida_xml(elem):
    """Formata o XML para ficar bonito (indentado)."""
    ElementTree.indent(elem, space="  ")
    return ElementTree.tostring(elem, encoding='unicode')

def grava_dados_xml():
    """Salva a estrutura atual do ElementTree no arquivo."""
    with open(nome_arquivo, 'w') as file_object:
        file_object.write(formata_saida_xml(clientesElement))

def ler_dados_xml():
    """Lê o arquivo XML e popula a listaClientes e o clientesElement."""
    global listaClientes, clientesElement
    try:
        with open(nome_arquivo, 'rt') as f:
            tree = ElementTree.parse(f)
            root = tree.getroot()

        listaClientes.clear()

        for cliente_xml in root.findall('cliente'):
            dict_cliente = {
                "id": int(cliente_xml.find('id').text),
                "nome": cliente_xml.find('nome').text,
                "cpf": cliente_xml.find('cpf').text,
                "historico": []
            }
            
            # Recupera o histórico (se houver itens salvos)
            historico_elem = cliente_xml.find('historico')
            if historico_elem:
                # Assumindo que o histórico guarda IDs de ingressos ou strings
                for item in historico_elem.findall('item'):
                    dict_cliente["historico"].append(item.text)

            listaClientes.append(dict_cliente)

        clientesElement = root

    except FileNotFoundError:
        # Se não existe, cria a estrutura básica
        clientesElement = Element('clientes')
        clientesElement.append(Comment('Dados de Clientes'))


def cadastra_cliente(nome: str, cpf: str) -> int:
    """
    cadastra um novo cliente no sistema
    retorno: 0 (sucesso), 2 (ja existe), -1 (invalido)
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

    # --- PERSISTÊNCIA XML  ---
    cliente_xml = SubElement(clientesElement, 'cliente')
    
    SubElement(cliente_xml, 'id').text = str(novo_cliente['id'])
    SubElement(cliente_xml, 'nome').text = novo_cliente['nome']
    SubElement(cliente_xml, 'cpf').text = novo_cliente['cpf']
    
    # Cria container para histórico
   

    grava_dados_xml()
    # ---------------------------------

    listaClientes.append(novo_cliente)
    return padrao_retornos.SUCESSO


def busca_cliente(id: int) -> dict | None:
    """
    busca um cliente específico pelo ID
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
    """

    return listaClientes[:] 


def remove_cliente(id: int) -> int:
    """
    remove um cliente do sistema
    retorno: 0 (sucesso), 1 (nao encontrado), -1 (invalido)
    """

    if not isinstance(id, int) or id <= 0:
        return padrao_retornos.PARAMETRO_INVALIDO

    for cliente in listaClientes:
        if cliente["id"] == id:
            
            # Remove da memória
            listaClientes.remove(cliente)
            
            # --- PERSISTÊNCIA XML (DELETE) ---
            str_id = str(id)
            for cli_xml in clientesElement.findall('cliente'):
                if cli_xml.find('id').text == str_id:
                    clientesElement.remove(cli_xml)
                    grava_dados_xml()
                    break
            # ---------------------------------

            return padrao_retornos.SUCESSO

    return padrao_retornos.NAO_ENCONTRADO


# Carrega os dados ao importar o módulo
ler_dados_xml()