import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path
from xml.etree.ElementTree import Element, Comment

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(TEST_DIR))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import padrao_retornos
import filme as f

class TestFilme(unittest.TestCase):
    """Testes para o módulo filme com isolamento de arquivos."""

    @classmethod
    def setUpClass(cls):
        """Executado uma vez antes de todos os testes."""
        # Salva referências originais
        cls.original_arquivo = f.nome_arquivo
        cls.original_element = f.filmesElement
        cls.original_lista = f.filmesEmCartaz.copy()

    def setUp(self):
        """Executado antes de cada teste."""
        # Cria diretório temporário para cada teste
        self.test_dir = tempfile.mkdtemp()
        self.test_arquivo = os.path.join(self.test_dir, "filmes_teste.xml")
        
        # Define ambiente de teste
        f.nome_arquivo = self.test_arquivo
        f.filmesEmCartaz  = []
        f.filmesElement = Element('filmes')
        comment = Comment('Dados de Filmes em Cartaz')
        f.filmesElement.append(comment)

    def tearDown(self):
        """Executado depois de cada teste."""
        # Remove diretório temporário
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @classmethod
    def tearDownClass(cls):
        """Executado uma vez depois de todos os testes."""
        # Restaura configurações originais
        f.nome_arquivo = cls.original_arquivo
        f.filmesElement = cls.original_element
        f.filmesEmCartaz = cls.original_lista

    # -------------------------
    # Testes para cria_filme()
    # -------------------------

    def test_01_cria_filme_ok_retorno(self):
        print("Caso de Teste 01 - Criar filme com sucesso (retorno 0)")
        retorno_esperado = f.cria_filme("Tropa de Elite", "Na favela do Rio de Janeiro, o Capitão Nascimento lidera uma equipe do BOPE em missões perigosas para combater o tráfico de drogas e a violência urbana. Enquanto enfrenta desafios tanto nas ruas quanto em sua vida pessoal, Nascimento luta para manter a ordem e proteger os inocentes em meio ao caos da cidade.", "Ação/Drama", 115.0, 18, "2007-10-05")
        
        self.assertEqual(retorno_esperado, 0)

    def test_02_cria_filme_nok_duplicado(self):
        print("Caso de Teste 02 - Impede a inserção com ID duplicado (retorno 2)")
        f.cria_filme("Interstellar", "As reservas naturais da Terra estão chegando ao fim e um grupo de astronautas recebe a missão de verificar possíveis planetas para receberem a população mundial, possibilitando a continuação da espécie. Cooper é chamado para liderar o grupo e aceita a missão sabendo que pode nunca mais ver os filhos. Ao lado de Brand, Jenkins e Doyle, ele seguirá em busca de um novo lar.", "Ficção Científica", 169.0, 10, "2014-11-06")
        retorno_esperado = f.cria_filme("Interstellar", "As reservas naturais da Terra estão chegando ao fim e um grupo de astronautas recebe a missão de verificar possíveis planetas para receberem a população mundial, possibilitando a continuação da espécie. Cooper é chamado para liderar o grupo e aceita a missão sabendo que pode nunca mais ver os filhos. Ao lado de Brand, Jenkins e Doyle, ele seguirá em busca de um novo lar.", "Ficção Científica", 169.0, 10, "2014-11-06")

        self.assertEqual(retorno_esperado, 2)

    def test_03_cria_filme_nok_parametros_invalidos(self):
        print("Caso de Teste 03 - Verifica parâmetros inválidos (retorno -1)")
        retorno_esperado = f.cria_filme(None, "Em um quarto de criança, os brinquedos ganham vida quando não há ninguém por perto. Woody, um boneco caubói, é o líder dos brinquedos e se sente ameaçado quando Buzz Lightyear, um moderno boneco astronauta, chega para disputar a atenção do garoto Andy. A rivalidade entre os dois brinquedos acaba levando-os a uma aventura inesperada, onde precisam aprender a trabalhar juntos para voltar para casa.", "Animação", "81.0", "L", "1995-11-22")

        self.assertEqual(retorno_esperado, -1)

    # # -------------------------
    # # Testes para busca_filme()
    # # -------------------------

    def test_04_busca_filme_ok_retorno_dict(self):
        print("Caso de Teste 04 - Buscar filme existente retorna dict")
        f.cria_filme("Procurando Nemo", "Após a captura de seu filho Nemo por um mergulhador, Marlin, um peixe-palhaço superprotetor, embarca em uma jornada épica pelo oceano para resgatá-lo. Com a ajuda de Dory, uma peixe cirurgiã esquecida, Marlin enfrenta diversos desafios e perigos marinhos enquanto aprende lições valiosas sobre confiança e coragem.", "Animação/Aventura", 100.0, 0, "2003-05-30")
        f.cria_filme("Procurando Dory", "Dory, a peixe cirurgiã esquecida, embarca em uma aventura para encontrar sua família perdida. Com a ajuda de seus amigos Marlin e Nemo, Dory enfrenta desafios no oceano e descobre a importância da amizade e da perseverança enquanto busca por suas raízes.", "Animação", 97.0, 0, "2016-06-17")
        retorno_esperado = f.busca_filme(2)

        self.assertEqual(retorno_esperado, {
            "id": 2,
            "titulo": "Procurando Dory",
            "sinopse": "Dory, a peixe cirurgiã esquecida, embarca em uma aventura para encontrar sua família perdida. Com a ajuda de seus amigos Marlin e Nemo, Dory enfrenta desafios no oceano e descobre a importância da amizade e da perseverança enquanto busca por suas raízes.",
            "genero": "Animação",
            "duracao": 97.0,
            "classificacao": 0,
            "dataLancamento": "17/06/2016"
        })

    def test_05_busca_filme_nok_nao_existe(self):
        print("Caso de Teste 05 - Buscar filme inexistente retorna None")
        retorno_esperado = f.busca_filme(21)
        self.assertEqual(retorno_esperado, None)

    def test_06_busca_filme_nok_parametro_invalido(self):
        print("Caso de Teste 06 - Buscar com parâmetro inválido retorna -1")
        resultado_esperado = f.busca_filme("abc")
        self.assertEqual(resultado_esperado, -1)

    # -------------------------
    # Testes para lista_filmes()
    # -------------------------

    def test_07_lista_filmes_vazia(self):
        print("Caso de Teste 07 - Lista vazia inicialmente")
        filmes_esperados = f.lista_filmes()
        self.assertEqual(filmes_esperados, [])

    def test_08_lista_filmes_com_elementos(self):
        print("Caso de Teste 08 - Lista com elementos (tamanho = 2)")
        f.cria_filme("Procurando Nemo", "Após a captura de seu filho Nemo por um mergulhador, Marlin, um peixe-palhaço superprotetor, embarca em uma jornada épica pelo oceano para resgatá-lo. Com a ajuda de Dory, uma peixe cirurgiã esquecida, Marlin enfrenta diversos desafios e perigos marinhos enquanto aprende lições valiosas sobre confiança e coragem.", "Animação/Aventura", 100.0, 0, "2003-05-30")
        f.cria_filme("Procurando Dory", "Dory, a peixe cirurgiã esquecida, embarca em uma aventura para encontrar sua família perdida. Com a ajuda de seus amigos Marlin e Nemo, Dory enfrenta desafios no oceano e descobre a importância da amizade e da perseverança enquanto busca por suas raízes.", "Animação", 97.0, 0, "2016-06-17")
        filmes_esperados = f.lista_filmes()
        self.assertEqual(len(filmes_esperados), 2)
        self.assertEqual(filmes_esperados, [
            {
                "id": 1,
                "titulo": "Procurando Nemo",
                "sinopse": "Após a captura de seu filho Nemo por um mergulhador, Marlin, um peixe-palhaço superprotetor, embarca em uma jornada épica pelo oceano para resgatá-lo. Com a ajuda de Dory, uma peixe cirurgiã esquecida, Marlin enfrenta diversos desafios e perigos marinhos enquanto aprende lições valiosas sobre confiança e coragem.",
                "genero": "Animação/Aventura",
                "duracao": 100.0,
                "classificacao": 0,
                "dataLancamento": "30/05/2003"
            },
            {
                "id": 2,
                "titulo": "Procurando Dory",
                "sinopse": "Dory, a peixe cirurgiã esquecida, embarca em uma aventura para encontrar sua família perdida. Com a ajuda de seus amigos Marlin e Nemo, Dory enfrenta desafios no oceano e descobre a importância da amizade e da perseverança enquanto busca por suas raízes.",
                "genero": "Animação",
                "duracao": 97.0,
                "classificacao": 0,
                "dataLancamento": "17/06/2016"
            }
        ])

    # -------------------------
    # Testes para remove_filme()
    # -------------------------

    def test_09_remove_filme_ok(self):
        print("Caso de Teste 09 - Remover filme existente (retorna 0)")
        f.cria_filme("Divertida Mente", "Riley é uma garota de 11 anos que enfrenta uma grande mudança em sua vida ao se mudar para uma nova cidade com seus pais. Dentro da mente de Riley, cinco emoções - Alegria, Tristeza, Raiva, Medo e Nojinho - trabalham juntas para guiá-la através dessa transição difícil. Quando Alegria e Tristeza se perdem na mente de Riley, as outras emoções precisam encontrar uma maneira de trazê-las de volta antes que Riley perca o controle de suas emoções.", "Animação/Aventura", 95.0, 0, "2015-06-19")
        retorno_esperado = f.remove_filme(1)
        retorno_busca_filme = f.busca_filme(1)
        self.assertEqual(retorno_esperado, 0)
        self.assertIsNone(retorno_busca_filme)

    def test_10_remove_filme_nok_id_inexistente(self):
        print("Caso de Teste 10 - Remover filme inexistente (retorna 1)")
        retorno_busca_filme = f.busca_filme(21)
        retorno_esperado = f.remove_filme(21)

        self.assertIsNone(retorno_busca_filme)
        self.assertEqual(retorno_esperado, 1)

    def test_11_remove_filme_nok_parametro_invalido(self):
        print("Caso de Teste 11 - Remover com parâmetro inválido (retorna -1)")
        retorno_esperado = f.remove_filme("abc")
        self.assertEqual(retorno_esperado, -1)

    # -------------------------
    # Testes para atualiza_dados_filme()
    # -------------------------

    def test_12_atualiza_filme_ok_titulo(self):
        print("Caso de Teste 12 - Atualizar apenas título (retorna 0)")
        f.cria_filme("O poderoso Chefão", "Na década de 1940, a família mafiosa Corleone, liderada por Vito Corleone, enfrenta desafios internos e externos enquanto luta para manter seu império criminoso. Quando Vito é alvo de um atentado, seu filho mais novo, Michael, inicialmente relutante em se envolver nos negócios da família, acaba assumindo o controle e se tornando um líder implacável. A história acompanha a ascensão de Michael ao poder e os sacrifícios que ele faz para proteger sua família.", "Crime/Drama", 175.0, 18, "1972-03-24")
        codigo_filme = 1
        filme = f.busca_filme(codigo_filme)

        self.assertEqual(filme["titulo"], "O Poderoso Chefão")

        retorno_esperado = f.atualiza_dados_filme(codigo_filme, "O Poderoso Chefão - Parte I", None)

        self.assertEqual(retorno_esperado, 0)
        self.assertEqual(filme["titulo"], "O Poderoso Chefão - Parte I")

    def test_test_13_atualiza_filme_ok_genero(self):
        print("Caso de Teste 13 - Atualizar apenas gênero (retorna 0)")
        f.cria_filme("Matrix", "Thomas Anderson, um programador de computador, descobre que a realidade em que vive é uma simulação criada por máquinas inteligentes para subjugar a humanidade. Ao ser libertado da Matrix por um grupo de rebeldes liderados por Morpheus, Thomas assume o papel de Neo, o escolhido para libertar a humanidade. Com habilidades extraordinárias dentro da Matrix, Neo enfrenta agentes implacáveis enquanto luta para desvendar a verdade sobre sua existência e salvar a humanidade.", "Ficção Científica/Ação", 136.0, 16, "1999-03-31")
        codigo_filme = 1
        filme = f.busca_filme(codigo_filme)

        self.assertEqual(filme["genero"], "Ficção Científica/Ação")

        retorno_esperado = f.atualiza_dados_filme(codigo_filme, None, "Ficção Científica")
        self.assertEqual(retorno_esperado, 0)
        self.assertEqual(filme["genero"], "Ficção Científica")

    def test_14_atualiza_filme_ok_titulo_e_genero(self):
        print("Caso de Teste 14 - Atualizar título e gênero juntos (retorna 0)")
        f.cria_filme("Gladiador", "Após a traição e assassinato de sua família pelo corrupto imperador Commodus, o general romano Maximus Decimus Meridius é reduzido à escravidão e se torna um gladiador. Determinado a vingar a morte de sua família e restaurar a justiça em Roma, Maximus luta em arenas sangrentas, conquistando a admiração do público e desafiando o poder do imperador. Sua jornada épica o leva a confrontar seus próprios demônios enquanto busca redenção e honra.", "Ação/Drama", 155.0, 16, "2000-05-05")
        codigo_filme = 1
        filme = f.busca_filme(codigo_filme)

        self.assertEqual(filme["titulo"], "Gladiador")
        self.assertEqual(filme["genero"], "Ação/Drama")

        retorno_esperado = f.atualiza_dados_filme(codigo_filme, "Gladiador - Edição Especial", "Ação")

        self.assertEqual(retorno_esperado, 0)
        self.assertEqual(filme["titulo"], "Gladiador - Edição Especial")
        self.assertEqual(filme["genero"], "Ação")

    def test_15_atualiza_filme_ok_nada(self):
        print("Caso de Teste 15 - Atualizar sem mudanças (retorna 0)")
        f.cria_filme("Clube da Luta", "Um homem insatisfeito com sua vida monótona encontra alívio ao formar um clube de luta clandestino com um vendedor de sabonetes carismático. À medida que o clube cresce, ele se torna uma força revolucionária que desafia as normas sociais e questiona a identidade do protagonista. No entanto, as consequências de suas ações começam a se desenrolar, levando a uma série de eventos imprevisíveis.", "Drama/Suspense", 139.0, 18, "1999-10-15")
        codigo_filme = 1
        filme = f.busca_filme(codigo_filme)

        self.assertEqual(filme["titulo"], "Clube Da Luta")
        self.assertEqual(filme["genero"], "Drama/Suspense")

        retorno_esperado = f.atualiza_dados_filme(codigo_filme, None, None)

        self.assertEqual(retorno_esperado, 0)
        self.assertEqual(filme["titulo"], "Clube Da Luta")
        self.assertEqual(filme["genero"], "Drama/Suspense")

    def test_16_atualiza_filme_nok_inexistente(self):
        print("Caso de Teste 16 - Atualizar filme inexistente (retorna 1)")
        retorno_esperado = f.atualiza_dados_filme(9999, "Novo Título", None)
        self.assertEqual(retorno_esperado, 1)

    def test_17_atualiza_filme_nok_parametro_invalido(self):
        print("Caso de Teste 17 - Atualizar com parâmetro inválido (retorna -1)")
        f.cria_filme("Clube da Luta", "Um homem insatisfeito com sua vida monótona encontra alívio ao formar um clube de luta clandestino com um vendedor de sabonetes carismático. À medida que o clube cresce, ele se torna uma força revolucionária que desafia as normas sociais e questiona a identidade do protagonista. No entanto, as consequências de suas ações começam a se desenrolar, levando a uma série de eventos imprevisíveis.", "Drama/Suspense", 139.0, 18, "1999-10-15")
        codigo_filme = 1

        retorno_esperado = f.atualiza_dados_filme(codigo_filme, 12345, None)

        self.assertEqual(retorno_esperado, -1)

if __name__ == "__main__":
    unittest.main()
