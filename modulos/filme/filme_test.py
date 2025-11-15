import filme

def test_criaFilme():
    filmeCriadoComSucesso = filme.criaFilme("Interstellar", "As reservas naturais da Terra estão chegando ao fim e um grupo de astronautas recebe a missão de verificar possíveis planetas para receberem a população mundial, possibilitando a continuação da espécie. Cooper é chamado para liderar o grupo e aceita a missão sabendo que pode nunca mais ver os filhos. Ao lado de Brand, Jenkins e Doyle, ele seguirá em busca de um novo lar.", "Ficção Científica", 169.0, 10, "2014-11-06")

    assert filmeCriadoComSucesso == 1, f"Esperado 1 mas retorna {filmeCriadoComSucesso}"

    filmeNaoCriado = filme.criaFilme(None, None, None, None, None, None)
    print(filmeNaoCriado)

    assert filmeNaoCriado == 0, f"Esperado 0 mas retorna {filmeNaoCriado}" 