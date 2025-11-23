# ingresso_test.py

import unittest
import sys
import os
from unittest.mock import patch
from xml.etree.ElementTree import Comment

# --------------------------------------------------------------------
# CONFIGURAÇÃO DE PATHS
# --------------------------------------------------------------------

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(TEST_DIR))

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import padrao_retornos
import modulos.ingresso.ingresso as modulo_ingresso

from modulos.ingresso.ingresso import (
    cria_ingresso,
    lista_ingressos_cliente,
    lista_ingressos_sessao,
    obtem_todos_ingressos,
    grava_dados_xml_ingresso,
    ingressosElement,
    listaIngressos
)

# --------------------------------------------------------------------
# TESTES DO MÓDULO INGRESSO
# --------------------------------------------------------------------

class TestIngressoCompleto(unittest.TestCase):

    def setUp(self):
        """Limpa XML + memória antes de cada teste."""
        
        # Limpa RAM
        listaIngressos.clear()

        # Limpa XML (raiz)
        ingressosElement.clear()
        ingressosElement.tag = "ingressos"
        ingressosElement.append(Comment("Dados de Ingressos do Sistema"))

        grava_dados_xml_ingresso()

    # ------------------------------------------------------------
    # TESTES DE CRIAÇÃO
    # ------------------------------------------------------------

    @patch("modulos.ingresso.ingresso.busca_cliente")
    @patch("modulos.ingresso.ingresso.busca_sessao")
    @patch("modulos.ingresso.ingresso.reserva_assento")
    def test_01_cria_ingresso_sucesso(self, mock_reserva, mock_busca_sessao, mock_busca_cliente):
        print("\nTeste 01: Criar ingresso com sucesso")

        mock_busca_cliente.return_value = {"id": 10}
        mock_busca_sessao.return_value = {"id": 5}
        mock_reserva.return_value = padrao_retornos.SUCESSO

        ret = cria_ingresso(10, 5, 20, 30.0)

        self.assertEqual(ret, padrao_retornos.SUCESSO)
        self.assertEqual(len(obtem_todos_ingressos()), 1)

    @patch("modulos.ingresso.ingresso.busca_cliente")
    def test_02_cria_ingresso_cliente_inexistente(self, mock_busca_cliente):
        print("Teste 02: Cliente inexistente")

        mock_busca_cliente.return_value = None

        ret = cria_ingresso(999, 1, 10, 25)
        self.assertEqual(ret, padrao_retornos.NAO_ENCONTRADO)
        self.assertEqual(len(obtem_todos_ingressos()), 0)

    @patch("modulos.ingresso.ingresso.busca_cliente")
    @patch("modulos.ingresso.ingresso.busca_sessao")
    def test_03_cria_ingresso_sessao_inexistente(self, mock_busca_sessao, mock_busca_cliente):
        print("Teste 03: Sessão inexistente")

        mock_busca_cliente.return_value = {"id": 10}
        mock_busca_sessao.return_value = None

        ret = cria_ingresso(10, 999, 10, 25)
        self.assertEqual(ret, padrao_retornos.NAO_ENCONTRADO)

    @patch("modulos.ingresso.ingresso.busca_cliente")
    @patch("modulos.ingresso.ingresso.busca_sessao")
    @patch("modulos.ingresso.ingresso.reserva_assento")
    def test_04_cria_ingresso_assento_ocupado(self, mock_reserva, mock_busca_sessao, mock_busca_cliente):
        print("Teste 04: Assento ocupado")

        mock_busca_cliente.return_value = {"id": 10}
        mock_busca_sessao.return_value = {"id": 5}
        mock_reserva.return_value = padrao_retornos.JA_EXISTE

        ret = cria_ingresso(10, 5, 5, 25)
        self.assertEqual(ret, padrao_retornos.JA_EXISTE)

    @patch("modulos.ingresso.ingresso.busca_cliente")
    @patch("modulos.ingresso.ingresso.busca_sessao")
    @patch("modulos.ingresso.ingresso.reserva_assento")
    def test_05_cria_ingresso_sessao_lotada(self, mock_reserva, mock_busca_sessao, mock_busca_cliente):
        print("Teste 05: Sessão lotada")

        mock_busca_cliente.return_value = {"id": 10}
        mock_busca_sessao.return_value = {"id": 5}
        mock_reserva.return_value = padrao_retornos.ERRO_SESSAO_LOTADA

        ret = cria_ingresso(10, 5, 7, 25)
        self.assertEqual(ret, padrao_retornos.ERRO_SESSAO_LOTADA)

    # ------------------------------------------------------------
    # LEITURA POR CLIENTE
    # ------------------------------------------------------------

    @patch("modulos.ingresso.ingresso.busca_cliente")
    def test_06_lista_ingressos_cliente_sem_ingressos(self, mock_busca_cliente):
        print("Teste 06: Cliente existe mas sem ingressos")

        mock_busca_cliente.return_value = {"id": 10}

        res = lista_ingressos_cliente(10)
        self.assertEqual(res, [])

    def test_07_lista_ingressos_cliente_inexistente(self):
        print("Teste 07: Cliente inexistente")

        res = lista_ingressos_cliente(-5)
        self.assertIsNone(res)

    # ------------------------------------------------------------
    # LEITURA POR SESSÃO
    # ------------------------------------------------------------

    @patch("modulos.ingresso.ingresso.busca_sessao")
    def test_08_lista_ingressos_sessao_inexistente(self, mock_busca_sessao):
        print("Teste 08: Sessão inexistente")

        mock_busca_sessao.return_value = None

        res = lista_ingressos_sessao(999)
        self.assertEqual(res, [])

    @patch("modulos.ingresso.ingresso.busca_sessao")
    def test_09_lista_ingressos_sessao_vazia(self, mock_busca_sessao):
        print("Teste 09: Sessão existe mas vazia")

        mock_busca_sessao.return_value = {"id": 5}

        res = lista_ingressos_sessao(5)
        self.assertEqual(res, [])

    # ------------------------------------------------------------
    # ACÚMULO
    # ------------------------------------------------------------

    @patch("modulos.ingresso.ingresso.busca_cliente", lambda cid: {"id": cid})
    @patch("modulos.ingresso.ingresso.busca_sessao", lambda sid: {"id": sid})
    @patch("modulos.ingresso.ingresso.reserva_assento", lambda *args: padrao_retornos.SUCESSO)
    def test_10_acumulo(self):
        print("Teste 10: Múltiplas vendas acumuladas")

        cria_ingresso(10, 1, 1, 20)
        cria_ingresso(11, 1, 2, 20)
        cria_ingresso(10, 2, 1, 20)

        self.assertEqual(len(obtem_todos_ingressos()), 3)


if __name__ == "__main__":
    unittest.main()
