import unittest
import sys
import os
from unittest.mock import patch


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(TEST_DIR))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import padrao_retornos
import modulos.sessao.sessao as modulo_sessao

from modulos.sessao.sessao import (
    cria_sessao, 
    busca_sessao, 
    assentos_disponiveis, 
    reserva_assento, 
    apaga_sessao, 
    obtem_todas_sessoes,
    ERRO_SESSAO_LOTADA
)


class TestSessaoCompleto(unittest.TestCase):

    def setUp(self):
        """Limpa apenas a lista de sessões local."""
        modulo_sessao.listaSessoes.clear()

    # -----------------------------------------------------------------------
    # TESTES DE CRIAÇÃO
    # -----------------------------------------------------------------------

    @patch('modulos.sessao.sessao.busca_filme') 
    def test_01_cria_sessao_sucesso(self, mock_busca_filme):
        print("\nTeste 01: Criar sessão com sucesso")
        mock_busca_filme.return_value = {"id": 1, "titulo": "Filme Teste"}

        retorno = cria_sessao(1, 5, "20:00", 100, "dublado")
        
        # Verificação
        self.assertEqual(retorno, padrao_retornos.SUCESSO)
        self.assertEqual(len(obtem_todas_sessoes()), 1)

    @patch('modulos.sessao.sessao.busca_filme')
    def test_02_cria_sessao_filme_inexistente(self, mock_busca_filme):
        print("Teste 02: Filme inexistente")
        
        mock_busca_filme.return_value = None

        retorno = cria_sessao(99, 5, "20:00", 100, "dublado")
        
        self.assertEqual(retorno, padrao_retornos.NAO_ENCONTRADO)
        self.assertEqual(len(obtem_todas_sessoes()), 0)

    @patch('modulos.sessao.sessao.busca_filme')
    def test_03_conflito_horario(self, mock_busca_filme):
        print("Teste 03: Conflito de horário")
        
        # MOCK: O filme sempre existe para esse teste
        mock_busca_filme.return_value = {"id": 1, "titulo": "Filme Teste"}

        # 1. Cria a primeira sessão
        cria_sessao(1, 5, "20:00", 100, "dublado")

        # 2. Tenta criar a segunda (Mesma sala/horario)
        retorno = cria_sessao(1, 5, "20:00", 100, "legendado")

        self.assertEqual(retorno, padrao_retornos.JA_EXISTE)

    # -----------------------------------------------------------------------
    # TESTES DE RESERVA
    # -----------------------------------------------------------------------

    @patch('modulos.sessao.sessao.busca_filme')
    def test_04_reserva_assento(self, mock_busca_filme):
        print("Teste 04: Fluxo de Reserva")
        mock_busca_filme.return_value = {"id": 1}
        
        # Cria sessão (ID 1)
        cria_sessao(1, 5, "20:00", 100, "dublado") 

        # Reserva
        retorno = reserva_assento(1, 10)
        
        self.assertEqual(retorno, padrao_retornos.SUCESSO)
        sessao = busca_sessao(1)
        self.assertIn(10, sessao["assentos_ocupados"])

    @patch('modulos.sessao.sessao.busca_filme')
    def test_05_reserva_assento_lotado(self, mock_busca_filme):
        print("Teste 05: Reserva em sessão lotada")
        mock_busca_filme.return_value = {"id": 10}
        
        # Cria sessão PEQUENA (Capacidade 1)
        cria_sessao(10, 1, "20:00", 1, "dublado") # ID 1
        reserva_assento(1, 1) # Assento válido 1

        ret = reserva_assento(1, 1) # Tenta o mesmo, ou outro, deve dar LOTADA primeiro

        self.assertEqual(ret, ERRO_SESSAO_LOTADA)
    
    @patch('modulos.sessao.sessao.busca_filme')
    def test_06_reserva_assento_ocupado(self, mock_busca_filme):
        print("Test 06: Falha ao reservar assento ocupado")
        mock_busca_filme.return_value = {"id": 1}

        cria_sessao(1, 5, "20:00", 100, "dublado")
        reserva_assento(1, 10)  

        # Tenta o mesmo assento
        retorno = reserva_assento(1, 10)
        self.assertEqual(retorno, padrao_retornos.JA_EXISTE)
    
    # -----------------------------------------------------------------------
    # TESTES DE LEITURA
    # -----------------------------------------------------------------------

    def test_07_assentos_sessao_inexistente(self):
        print("Teste 07: Assentos de sessão inexistente")
        # Não precisamos de mock aqui pois busca_sessao só olha a lista local
        qtd = assentos_disponiveis(999)
        self.assertEqual(qtd, -1)

    @patch('modulos.sessao.sessao.busca_filme')
    def test_08_assentos_sessao_lotada(self, mock_busca_filme):
        print("Teste 08: Assentos de sessão lotada")
        mock_busca_filme.return_value = {"id": 50}
        
        # Cria sessão capacidade 2
        cria_sessao(50, 2, "20:00", 2, "dublado") # ID 1
        
        # Ocupa tudo
        reserva_assento(1, 1)
        reserva_assento(1, 2)
        
        qtd = assentos_disponiveis(1)
        self.assertEqual(qtd, 0)

    @patch('modulos.sessao.sessao.busca_filme')
    def test_09_assentos_sessao_vazia(self, mock_busca_filme):
        print("Teste 09: Assentos de sessão vazia")
        mock_busca_filme.return_value = {"id": 51}
        
        cria_sessao(51, 1, "20:00", 100, "dublado")
        
        qtd = assentos_disponiveis(1)
        self.assertEqual(qtd, 100)

    # -----------------------------------------------------------------------
    # TESTES DE VALIDAÇÃO
    # -----------------------------------------------------------------------

    @patch('modulos.sessao.sessao.busca_filme')
    def test_10_validacao_sucesso_mesma_sala_horario_diferente(self, mock_busca_filme):
        print("Teste 10: Sucesso - Mesma sala, horário diferente")
        mock_busca_filme.return_value = {"id": 1}
        
        cria_sessao(1, 1, "10:00", 50, "dublado")
        retorno = cria_sessao(1, 1, "12:00", 50, "dublado")
        
        self.assertEqual(retorno, padrao_retornos.SUCESSO)
        self.assertEqual(len(obtem_todas_sessoes()), 2)

    @patch('modulos.sessao.sessao.busca_filme')
    def test_11_validacao_sucesso_sala_diferente_mesmo_horario(self, mock_busca_filme):
        print("Teste 11: Sucesso - Sala diferente, mesmo horário")
        mock_busca_filme.return_value = {"id": 1}
        
        cria_sessao(1, 1, "10:00", 50, "dublado")
        retorno = cria_sessao(1, 2, "10:00", 50, "dublado")
        
        self.assertEqual(retorno, padrao_retornos.SUCESSO)
        self.assertEqual(len(obtem_todas_sessoes()), 2)

    @patch('modulos.sessao.sessao.busca_filme')
    def test_12_cria_sessao_horario_invalido(self, mock_busca_filme):
        print("Teste 12: Validação de formato de horário")
        mock_busca_filme.return_value = {"id": 1}

        self.assertEqual(cria_sessao(1, 5, "9:00", 100, "dublado"), padrao_retornos.PARAMETRO_INVALIDO)
        self.assertEqual(cria_sessao(1, 5, "HH:MM", 100, "dublado"), padrao_retornos.PARAMETRO_INVALIDO)
        self.assertEqual(cria_sessao(1, 5, "25:00", 100, "dublado"), padrao_retornos.PARAMETRO_INVALIDO)
        
        ret5 = cria_sessao(1, 5, "09:00", 100, "dublado")
        self.assertEqual(ret5, padrao_retornos.SUCESSO)

    # -----------------------------------------------------------------------
    # TESTES DE FILTROS
    # -----------------------------------------------------------------------

    @patch('modulos.sessao.sessao.busca_filme')
    def test_13_lista_sessoes_sem_filtro(self, mock_busca_filme):
        print("Test 13: Listar tudo")
        mock_busca_filme.return_value = {"id": 1} # Mock genérico

        cria_sessao(10, 1, "14:00", 100, "dublado")
        cria_sessao(10, 2, "20:00", 100, "legendado")
        cria_sessao(20, 1, "18:00", 100, "dublado")

        codigo, resultado = modulo_sessao.lista_sessoes()
        self.assertEqual(len(resultado), 3)

    @patch('modulos.sessao.sessao.busca_filme')
    def test_14_lista_sessoes_filtro_filme(self, mock_busca_filme):
        print("Test Lista 14: Filtro por Filme")
        mock_busca_filme.return_value = {"id": 1}

        cria_sessao(10, 1, "14:00", 100, "dublado")
        cria_sessao(20, 1, "16:00", 100, "dublado")

        codigo, resultado = modulo_sessao.lista_sessoes(filtro_filme_id=10)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["filme_id"], 10)

    @patch('modulos.sessao.sessao.busca_filme')
    def test_15_lista_sessoes_filtro_formato(self, mock_busca_filme):
        print("Test Lista 15: Filtro por Formato")
        mock_busca_filme.return_value = {"id": 1}

        cria_sessao(1, 1, "14:00", 100, "dublado")
        cria_sessao(1, 2, "16:00", 100, "legendado")

        codigo, resultado = modulo_sessao.lista_sessoes(formato_exibicao="legendado")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["formato_exibicao"], "legendado")

    @patch('modulos.sessao.sessao.busca_filme')
    def test_16_lista_sessoes_filtro_horario(self, mock_busca_filme):
        print("Test Lista 16: Filtro por Horário")
        mock_busca_filme.return_value = {"id": 1}

        cria_sessao(1, 1, "14:00", 100, "dublado") 
        cria_sessao(1, 2, "18:00", 100, "dublado")
        cria_sessao(1, 3, "20:00", 100, "dublado") 

        codigo, resultado = modulo_sessao.lista_sessoes(horario_minimo="18:00")

        self.assertEqual(len(resultado), 2)
        horarios = [s["horario"] for s in resultado]
        self.assertIn("18:00", horarios)
        self.assertIn("20:00", horarios)

    @patch('modulos.sessao.sessao.busca_filme')
    def test_17_filtros_combinados_vazio(self, mock_busca_filme):
        print("Test Lista 17: Filtros combinados vazio")
        mock_busca_filme.return_value = {"id": 1}

        cria_sessao(10, 1, "14:00", 100, "dublado")
        cria_sessao(20, 2, "20:00", 100, "dublado")

        codigo, resultado = modulo_sessao.lista_sessoes(filtro_filme_id=10, horario_minimo="18:00")
        self.assertEqual(resultado, []) 

    @patch('modulos.sessao.sessao.busca_filme')
    def test_18_filtros_combinados_preenchido(self, mock_busca_filme):
        print("Test 18: Filtros combinados sucesso")
        mock_busca_filme.return_value = {"id": 1}
        
        cria_sessao(10, 1, "14:00", 100, "dublado")
        cria_sessao(20, 2, "20:00", 100, "legendado")
        cria_sessao(10, 3, "19:00", 100, "dublado") # ID 3: Bate com tudo

        codigo, resultado = modulo_sessao.lista_sessoes(filtro_filme_id=10, horario_minimo="18:00")
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["id"], 3) 

    # -----------------------------------------------------------------------
    # TESTES DE EXCLUSÃO
    # -----------------------------------------------------------------------

    @patch('modulos.sessao.sessao.busca_filme')
    def test_19_apaga_sessao_sucesso(self, mock_busca_filme):
        print("Test 19: Apagar sessão sucesso")
        mock_busca_filme.return_value = {"id": 1}
        
        cria_sessao(10, 1, "14:00", 100, "dublado") # ID 1

        retorno = apaga_sessao(1)

        self.assertEqual(retorno, padrao_retornos.SUCESSO)
        self.assertEqual(len(obtem_todas_sessoes()), 0)

    @patch('modulos.sessao.sessao.busca_filme')
    def test_20_apaga_sessao_com_vendas(self, mock_busca_filme):
        print("Test 20: Bloquear apagamento com vendas")
        mock_busca_filme.return_value = {"id": 1}
        
        cria_sessao(10, 1, "14:00", 100, "dublado") # ID 1
        reserva_assento(1, 50)

        retorno = apaga_sessao(1)

        self.assertEqual(retorno, padrao_retornos.JA_EXISTE) 
        self.assertEqual(len(obtem_todas_sessoes()), 1) 

    def test_21_apaga_sessao_inexistente(self):
        print("Test 21: Apagar sessão inexistente")
        retorno = apaga_sessao(999)
        self.assertEqual(retorno, padrao_retornos.NAO_ENCONTRADO)

if __name__ == '__main__':
    unittest.main()