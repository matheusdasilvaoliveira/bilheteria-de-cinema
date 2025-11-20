import unittest
import sys
import os

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(TEST_DIR))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import padrao_retornos
import modulos.cliente.cliente as cliente_mod
from modulos.cliente.cliente import (
    cadastra_cliente,
    busca_cliente,
    lista_clientes,
    remove_cliente
)


# ------- MOCKS (se necessário para busca_cliente — mas aqui usamos a lista real) -------

def cliente_fake(id):
    if id == 1:
        return {"id": 1, "nome": "Teste", "cpf": "123", "historico": []}
    return None


class TestCliente(unittest.TestCase):

    def setUp(self):
        """
        Executado antes de cada teste.
        Limpa a listaClientes para garantir independência.
        """
        self.old_lista = cliente_mod.listaClientes
        cliente_mod.listaClientes = []

    def tearDown(self):
        """
        Restaura lista original.
        """
        cliente_mod.listaClientes = self.old_lista

    # ----------------------------------------------------------
    # TESTES cadastra_cliente
    # ----------------------------------------------------------

    def test_01_cadastro_sucesso(self):
        print("\nTest 01: Cadastro com sucesso")
        ret = cadastra_cliente("Fulano", "111")
        self.assertEqual(ret, padrao_retornos.SUCESSO)
        self.assertEqual(len(cliente_mod.listaClientes), 1)

    def test_02_cpf_duplicado(self):
        print("Test 02: CPF duplicado")
        cadastra_cliente("Fulano", "111")
        ret = cadastra_cliente("Beltrano", "111")
        self.assertEqual(ret, padrao_retornos.JA_EXISTE)
        self.assertEqual(len(cliente_mod.listaClientes), 1)

    def test_03_parametro_invalido(self):
        print("Test 03: Parâmetro inválido")
        ret = cadastra_cliente("", "123")
        self.assertEqual(ret, padrao_retornos.PARAMETRO_INVALIDO)

        ret = cadastra_cliente("Fulano", "")
        self.assertEqual(ret, padrao_retornos.PARAMETRO_INVALIDO)

    # ----------------------------------------------------------
    # TESTES busca_cliente
    # ----------------------------------------------------------

    def test_04_busca_cliente_existente(self):
        print("Test 04: Busca cliente existente")
        cadastra_cliente("Fulano", "111")
        cliente = busca_cliente(1)
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente["nome"], "Fulano")

    def test_05_busca_cliente_inexistente(self):
        print("Test 05: Busca cliente inexistente")
        cliente = busca_cliente(99)
        self.assertIsNone(cliente)

    def test_06_busca_cliente_parametro_invalido(self):
        print("Test 06: Busca cliente com parâmetro inválido")
        cliente = busca_cliente(-5)
        self.assertIsNone(cliente)

    # ----------------------------------------------------------
    # TESTES lista_clientes
    # ----------------------------------------------------------

    def test_07_lista_vazia(self):
        print("Test 07: Lista vazia")
        lista = lista_clientes()
        self.assertEqual(lista, [])

    def test_08_lista_com_itens(self):
        print("Test 08: Lista com itens")
        cadastra_cliente("Fulano", "111")
        cadastra_cliente("Beltrano", "222")

        lista = lista_clientes()

        self.assertEqual(len(lista), 2)
        self.assertTrue(any(c["nome"] == "Fulano" for c in lista))
        self.assertTrue(any(c["nome"] == "Beltrano" for c in lista))

    # ----------------------------------------------------------
    # TESTES remove_cliente
    # ----------------------------------------------------------

    def test_09_remove_cliente_sucesso(self):
        print("Test 09: Remoção com sucesso")
        cadastra_cliente("Fulano", "111")
        ret = remove_cliente(1)
        self.assertEqual(ret, padrao_retornos.SUCESSO)
        self.assertEqual(len(cliente_mod.listaClientes), 0)

    def test_10_remove_cliente_inexistente(self):
        print("Test 10: Remoção de cliente inexistente")
        ret = remove_cliente(99)
        self.assertEqual(ret, padrao_retornos.NAO_ENCONTRADO)

    def test_11_remove_cliente_parametro_invalido(self):
        print("Test 11: Remoção com parâmetro inválido")
        ret = remove_cliente(-1)
        self.assertEqual(ret, padrao_retornos.PARAMETRO_INVALIDO)


if __name__ == "__main__":
    unittest.main()
