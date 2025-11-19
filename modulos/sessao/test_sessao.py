import unittest
import sys
import os


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
    ERRO_SESSAO_LOTADA
)


def busca_filme_mentira(filme_id):
    """
    Esta função finge ser o módulo de filmes.
    Regra simples:
    - ID 1: Existe (Retorna um filme)
    - Qualquer outro ID: Não existe (Retorna None)
    """
    if filme_id == 1:
        return {"id": 1, "titulo": "Filme de Teste"}
    return None


class TestSessao(unittest.TestCase):

    def setUp(self):
        """
        RODA ANTES DE CADA TESTE.
        Faz a troca das funções reais pelas de mentira.
        """
        #  Backup das originais (para não quebrar o programa real)
        self.busca_filme_original = modulo_sessao.busca_filme
        self.lista_sessoes_original = modulo_sessao.listaSessoes

        modulo_sessao.busca_filme = busca_filme_mentira
        modulo_sessao.listaSessoes = []

    def tearDown(self):
        """
        RODA DEPOIS DE CADA TESTE.
        Devolve as funções originais para o módulo.
        """
        modulo_sessao.busca_filme = self.busca_filme_original
        modulo_sessao.listaSessoes = self.lista_sessoes_original


    def test_01_cria_sessao_sucesso(self):
        print("\nTeste 01: Criar sessão com filme existente (ID 1)")
        
        #ID 1, busca_filme_mentira diz que existe
        retorno = cria_sessao(1, 5, "20:00", 100, "dublado")
        
        self.assertEqual(retorno, padrao_retornos.SUCESSO)
        self.assertEqual(len(modulo_sessao.listaSessoes), 1)

    def test_02_cria_sessao_filme_inexistente(self):
        print("Teste 02: Tentar criar com filme inexistente (ID 99)")
        
        # ID 99, busca_filme_mentira encontra  None
        retorno = cria_sessao(99, 5, "20:00", 100, "dublado")
        
        self.assertEqual(retorno, padrao_retornos.NAO_ENCONTRADO)
        self.assertEqual(len(modulo_sessao.listaSessoes), 0)

    def test_03_conflito_horario(self):
        print("Teste 03: Testar conflito de horário")
        
        
        sessao_existente = {
            "id": 1, "filme_id": 1, "sala": 5, "horario": "20:00",
            "capacidade": 100, "formato_exibicao": "dublado", "assentos_ocupados": []
        }
        modulo_sessao.listaSessoes.append(sessao_existente)

        # Tentamos criar outra na mesma sala/hora 
        retorno = cria_sessao(1, 5, "20:00", 100, "legendado")

        self.assertEqual(retorno, padrao_retornos.JA_EXISTE)

    def test_04_reserva_assento(self):
        print("Teste 04: Fluxo de Reserva de Assento")
        
       
        cria_sessao(1, 5, "20:00", 100, "dublado") 

        # Reserva válida
        ret = reserva_assento(1, 10)
        self.assertEqual(ret, padrao_retornos.SUCESSO)

        # Verificar se salvou
        sessao = busca_sessao(1)
        self.assertIn(10, sessao["assentos_ocupados"])

    def test_05_reserva_assento_lotado(self):
        print("Teste 05: Reserva em sessão lotada")
        
        # Criamos sessão com capacidade 1
        modulo_sessao.listaSessoes.append({
            "id": 10, "capacidade": 1, "assentos_ocupados": [5] # Já cheia
        })

        # Tenta reservar outro
        ret = reserva_assento(10, 6)
        self.assertEqual(ret, ERRO_SESSAO_LOTADA)
    
    def test_09_assentos_sessao_inexistente(self):
        print("Teste 09: Assentos de sessão que não existe")
        # Tenta buscar assentos de um ID que não está na lista
        qtd = assentos_disponiveis(999)
        self.assertEqual(qtd, -1)

    def test_10_assentos_sessao_lotada(self):
        print("Teste 10: Assentos de sessão lotada (deve ser 0)")
        # Cria uma sessão com capacidade 2 e 2 ocupados
        modulo_sessao.listaSessoes.append({
            "id": 50, 
            "capacidade": 2, 
            "assentos_ocupados": [1, 2]
        })
        
        qtd = assentos_disponiveis(50)
        self.assertEqual(qtd, 0)

    def test_11_assentos_sessao_vazia(self):
        print("Teste 11: Assentos de sessão vazia (deve ser igual a capacidade)")
        modulo_sessao.listaSessoes.append({
            "id": 51, 
            "capacidade": 100, 
            "assentos_ocupados": []
        })
        
        qtd = assentos_disponiveis(51)
        self.assertEqual(qtd, 100)

    def test_12_validacao_sucesso_mesma_sala_horario_diferente(self):
        print("Teste 12: Sucesso - Mesma sala, horário diferente")
        # Cria a primeira: Sala 1 às 10:00
        cria_sessao(1, 1, "10:00", 50, "dublado")
        
        # Tenta criar a segunda: Sala 1 às 12:00 (Deve permitir!)
        retorno = cria_sessao(1, 1, "12:00", 50, "dublado")
        
        self.assertEqual(retorno, padrao_retornos.SUCESSO)
        self.assertEqual(len(modulo_sessao.listaSessoes), 2)

    def test_13_validacao_sucesso_sala_diferente_mesmo_horario(self):
        print("Teste 13: Sucesso - Sala diferente, mesmo horário")
        # Cria a primeira: Sala 1 às 10:00
        cria_sessao(1, 1, "10:00", 50, "dublado")
        
        # Tenta criar a segunda: Sala 2 às 10:00 
        retorno = cria_sessao(1, 2, "10:00", 50, "dublado")
        
        self.assertEqual(retorno, padrao_retornos.SUCESSO)
        self.assertEqual(len(modulo_sessao.listaSessoes), 2)

if __name__ == '__main__':
    unittest.main()