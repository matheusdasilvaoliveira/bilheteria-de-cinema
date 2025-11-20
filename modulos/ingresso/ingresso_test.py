import unittest
import sys
import os

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(TEST_DIR))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import padrao_retornos
import modulos.ingresso.ingresso as modulo_ingresso
import modulos.ingresso.ingresso as ingresso_mod

from modulos.ingresso.ingresso import (
    cria_ingresso,
    lista_ingressos_cliente,
    lista_ingressos_sessao
)

# mock
def busca_cliente_fake(cliente_id):
    if cliente_id == 1:
        return {"id": 1, "nome": "Fulano"}
    return None

def busca_sessao_fake(sessao_id):
    if sessao_id == 1:
        return {
            "id": 1,
            "capacidade": 5,
            "assentos_ocupados": []
        }
    return None

def reserva_assento_fake(sessao_id, numero_assento):
    if sessao_id != 1:
        return padrao_retornos.NAO_ENCONTRADO
    
    # Simula assento fora do range
    if numero_assento <= 0 or numero_assento > 5:
        return padrao_retornos.PARAMETRO_INVALIDO
    
    # Assento já ocupado?
    sessao = busca_sessao_fake(sessao_id)
    if numero_assento in sessao["assentos_ocupados"]:
        return padrao_retornos.JA_EXISTE

    # Sessão lotada?
    if len(sessao["assentos_ocupados"]) >= sessao["capacidade"]:
        return padrao_retornos.ERRO_SESSAO_LOTADA

    # Caso sucesso
    sessao["assentos_ocupados"].append(numero_assento)
    return padrao_retornos.SUCESSO


class TestIngresso(unittest.TestCase):

    def setUp(self):
        """
        Roda antes de cada teste.
        Troca busca_cliente, busca_sessao e reserva_assento pelas versões fake.
        E limpa a lista de ingressos.
        """
        self.old_busca_cliente = ingresso_mod.busca_cliente
        self.old_busca_sessao = ingresso_mod.busca_sessao
        self.old_reserva_assento = ingresso_mod.reserva_assento
        self.old_lista = ingresso_mod.listaIngressos

        ingresso_mod.busca_cliente = busca_cliente_fake
        ingresso_mod.busca_sessao = busca_sessao_fake
        ingresso_mod.reserva_assento = reserva_assento_fake

        ingresso_mod.listaIngressos = []

    def tearDown(self):
        """
        Roda depois de cada teste.
        Restaura as versões originais das funções.
        """
        ingresso_mod.busca_cliente = self.old_busca_cliente
        ingresso_mod.busca_sessao = self.old_busca_sessao
        ingresso_mod.reserva_assento = self.old_reserva_assento
        ingresso_mod.listaIngressos = self.old_lista


    # TESTES CRIA_INGRESSO

    def test_01_ingresso_sucesso(self):
        print("\nTest 01: Criação de ingresso com sucesso")
        ret = cria_ingresso(1, 1, 2, 30.0)
        self.assertEqual(ret, padrao_retornos.SUCESSO)
        self.assertEqual(len(ingresso_mod.listaIngressos), 1)

    def test_02_cliente_inexistente(self):
        print("Test 02: Cliente inexistente")
        ret = cria_ingresso(99, 1, 2, 30.0)
        self.assertEqual(ret, padrao_retornos.NAO_ENCONTRADO)
        self.assertEqual(len(ingresso_mod.listaIngressos), 0)

    def test_03_sessao_inexistente(self):
        print("Test 03: Sessão inexistente")
        ret = cria_ingresso(1, 99, 2, 30.0)
        self.assertEqual(ret, padrao_retornos.NAO_ENCONTRADO)

    def test_04_assento_ocupado(self):
        print("Test 04: Assento ocupado")
        cria_ingresso(1, 1, 2, 30.0)
        ret = cria_ingresso(1, 1, 2, 30.0)
        self.assertEqual(ret, padrao_retornos.JA_EXISTE)

    def test_05_sessao_lotada(self):
        print("Test 05: Sessão lotada")
        for i in range(1, 6):
            cria_ingresso(1, 1, i, 15.0)

        ret = cria_ingresso(1, 1, 6, 15.0)
        self.assertEqual(ret, padrao_retornos.ERRO_SESSAO_LOTADA)

    def test_06_parametro_invalido(self):
        print("Test 06: Parâmetro inválido")
        ret = cria_ingresso("abc", 1, 1, 20.0)
        self.assertEqual(ret, padrao_retornos.PARAMETRO_INVALIDO)


    # TESTES lista_ingressos_cliente

    def test_07_lista_cliente_com_ingressos(self):
        print("Test 07: Cliente com ingressos")
        cria_ingresso(1, 1, 1, 20.0)
        cria_ingresso(1, 1, 2, 20.0)

        lista = lista_ingressos_cliente(1)

        self.assertEqual(len(lista), 2)
        self.assertTrue(all(item["cliente_id"] == 1 for item in lista))

    def test_08_lista_cliente_sem_ingressos(self):
        print("Test 08: Cliente sem ingressos")
        lista = lista_ingressos_cliente(1)
        self.assertEqual(lista, [])

    def test_09_cliente_inexistente_lista(self):
        print("Test 09: Cliente inexistente na consulta")
        lista = lista_ingressos_cliente(99)
        self.assertIsNone(lista)


    # TESTES lista_ingressos_sessao

    def test_10_lista_sessao_com_ingressos(self):
        print("Test 10: Sessão com ingressos")
        cria_ingresso(1, 1, 1, 20.0)
        cria_ingresso(1, 1, 2, 20.0)

        lista = lista_ingressos_sessao(1)
        self.assertEqual(len(lista), 2)
        self.assertTrue(all(item["sessao_id"] == 1 for item in lista))

    def test_11_lista_sessao_sem_ingressos(self):
        print("Test 11: Sessão sem ingressos")
        lista = lista_ingressos_sessao(1)
        self.assertEqual(lista, [])

    def test_12_sessao_inexistente_em_lista(self):
        print("Test 12: Sessão inexistente na consulta")
        lista = lista_ingressos_sessao(999)
        self.assertEqual(lista, [])


if __name__ == "__main__":
    unittest.main()

