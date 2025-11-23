import unittest
from unittest.mock import patch

import modulos.monitoramento.monitoramento as mon


class TestMonitoramento(unittest.TestCase):

    def setUp(self):
        # Garante que a lista de ingressos começa vazia
        mon.listaIngressos.clear()

    # -----------------------------------------
    # TESTE 01 – Filme inexistente
    # -----------------------------------------
    @patch("modulos.monitoramento.monitoramento.busca_filme")
    def test_01_filme_inexistente(self, mock_filme):
        mock_filme.return_value = None

        r = mon.receita_e_ingressos(10)
        self.assertIsNone(r)

    # -----------------------------------------
    # TESTE 02 – Filme existe mas não tem vendas
    # -----------------------------------------
    @patch("modulos.monitoramento.monitoramento.busca_filme")
    @patch("modulos.monitoramento.monitoramento.busca_sessao")
    def test_02_filme_sem_ingressos(self, mock_sessao, mock_filme):

        mock_filme.return_value = {"id": 5, "titulo": "Filme X"}

        # Sessão existe, mas não vamos criar ingressos
        mock_sessao.return_value = {"id": 99, "filme_id": 5}

        r = mon.receita_e_ingressos(5)
        self.assertIsNone(r)

    # -----------------------------------------
    # TESTE 03 – Várias sessões e ingressos
    # -----------------------------------------
    @patch("modulos.monitoramento.monitoramento.busca_filme")
    @patch("modulos.monitoramento.monitoramento.busca_sessao")
    def test_03_calculo_receita(self, mock_sessao, mock_filme):

        mock_filme.return_value = {"id": 1, "titulo": "Filme Teste"}

        # Mock de sessões
        def fake_busca_sessao(id_sessao):
            fake = {
                10: {"id": 10, "filme_id": 1},
                20: {"id": 20, "filme_id": 1},
                30: {"id": 30, "filme_id": 999}  # outra filme -> ignorar
            }
            return fake.get(id_sessao, None)

        mock_sessao.side_effect = fake_busca_sessao

        # popula ingressos (NÃO depende do módulo real)
        mon.listaIngressos.clear()
        mon.listaIngressos.extend([
            {"id": 1, "cliente_id": 7, "sessao_id": 10, "numero_assento": 1, "preco": 20},
            {"id": 2, "cliente_id": 8, "sessao_id": 20, "numero_assento": 2, "preco": 30},
            {"id": 3, "cliente_id": 9, "sessao_id": 30, "numero_assento": 3, "preco": 50}, # ignorado
        ])

        r = mon.receita_e_ingressos(1)

        self.assertEqual(r["ingressos_vendidos"], 2)
        self.assertEqual(r["receita"], 50.0)   # 20 + 30

if __name__ == "__main__":
    unittest.main()
