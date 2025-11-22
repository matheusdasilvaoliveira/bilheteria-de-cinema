import modulos.cliente.cliente as Cliente
import modulos.ingresso.ingresso as Ingresso
import modulos.sessao.sessao as Sessao
import modulos.filme.filme as Filme
import modulos.monitoramento.monitoramento as Monitoramento
import padrao_retornos
import sys
import os

# --- Correção de Caminho (Para garantir que imports funcionem) ---
# Adiciona a pasta raiz ao path para importar os módulos corretamente
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

def menu_filmes():
    while True:
        print("\n" + "-"*30)
        print("     GERENCIAR FILMES     ")
        print("-" * 30)
        print("1 - Cadastrar novo filme")
        print("2 - Listar filmes")
        print("3 - Buscar filme por ID")
        print("4 - Atualizar dados do filme")
        print("5 - Remover filme")
        print("0 - Voltar")
        print("-" * 30)
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n--- Novo Filme ---")
            try:
                # Coleta os dados solicitados
                id_filme = int(input("ID do Filme: "))
                titulo = input("Título: ")
                genero = input("Gênero: ")
                duracao = float(input("Duração (min): "))
                classificacao = int(input("Classificação Indicativa (anos): "))
                sinopse = input("Sinopse: ")
                data_lancamento = input("Data de Lançamento (AAAA-MM-DD): ")

                # Chama a função do módulo
                codigo_retorno = Filme.cria_filme(
                    id_filme, titulo, genero, duracao, 
                    classificacao, sinopse, data_lancamento
                )
                
                padrao_retornos.imprime_mensagem(codigo_retorno)
                
            except ValueError:
                print("Erro: Verifique se digitou números corretamente para ID, Duração e Classificação.")

        elif opcao == '2':
            print("\n--- Catálogo de Filmes ---")
            # Chama a função de listagem
            lista = Filme.lista_filmes()
            
            if not lista:
                print("Nenhum filme cadastrado.")
            else:
                print("-" * 90)
                print(f"{'ID':<5} | {'Título':<20} | {'Gênero':<12} | {'Dur.':<6} | {'Class.':<6} | {'Lançamento'}")
                print("-" * 90)
                for f in lista:
                    data_obj = f.get('dataLancamento')
                    data_str = str(data_obj) if data_obj else "N/A"
                    classif_raw = f.get('classificacao')
                    classif_str = f"{classif_raw} anos" if classif_raw else "Livre"
                    titulo = f.get('titulo', 'Sem Título')[:20] 
                    genero = f.get('genero', 'N/A')[:12]
                    duracao = f.get('duracao', 0)
                    
                    print(f"{f['id']:<5} | {titulo:<20} | {genero:<12} | {duracao:<6} | {classif_str:<6} | {data_str}")
                
                print("-" * 90)

        elif opcao == '3':
            print("\n--- Buscar Filme ---")
            try:
                id_busca = int(input("Digite o ID do filme: "))
                
                filme_encontrado = Filme.busca_filme(id_busca)
                
                if filme_encontrado:
                    print("\n" + "="*30)
                    print(f"DETALHES DO FILME #{filme_encontrado['id']}")
                    print("="*30)
                    print(f"Título:        {filme_encontrado['titulo']}")
                    print(f"Gênero:        {filme_encontrado['genero']}")
                    print(f"Duração:       {filme_encontrado['duracao']} min")
                    print(f"Classificação: {filme_encontrado['classificacao']} anos")
                    print(f"Lançamento:    {filme_encontrado.get('dataLancamento', 'N/A')}")
                    print("-" * 30)
                    print(f"Sinopse:\n{filme_encontrado['sinopse']}")
                    print("="*30)
                else:
                    padrao_retornos.imprime_mensagem(padrao_retornos.NAO_ENCONTRADO)
                    
            except ValueError:
                print("Erro: O ID deve ser um número.")

        elif opcao == '4':
            print("\n--- Atualizar Filme ---")
            try:
                id_atualiza = int(input("Digite o ID do filme para atualizar: "))
                
                # Verifica se existe antes de pedir os dados (Opcional, mas boa prática de UX)
                if Filme.busca_filme(id_atualiza):
                    print("Deixe em branco para manter o valor atual.")
                    novo_titulo = input("Novo Título: ").strip()
                    novo_genero = input("Novo Gênero: ").strip()
                    
                    # Converte vazio para None, para a função saber que não deve alterar
                    val_titulo = novo_titulo if novo_titulo else None
                    val_genero = novo_genero if novo_genero else None

                    codigo_retorno = Filme.atualiza_dados_filme(id_atualiza, val_titulo, val_genero)
                    padrao_retornos.imprime_mensagem(codigo_retorno)
                else:
                    padrao_retornos.imprime_mensagem(padrao_retornos.NAO_ENCONTRADO)

            except ValueError:
                print("Erro: ID inválido.")

        elif opcao == '5':
            print("\n--- Remover Filme ---")
            try:
                id_remove = int(input("Digite o ID do filme para remover: "))
                codigo_retorno = Filme.remove_filme(id_remove)
                padrao_retornos.imprime_mensagem(codigo_retorno)
                
            except ValueError:
                print("Erro: O ID deve ser um número.")

        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

def menu_ingressos():
    while True:
        print("\n" + "-"*30)
        print("     GERENCIAR INGRESSOS     ")
        print("-" * 30)
        print("1 - Vender Ingresso")
        print("2 - Listar ingressos de um Cliente")
        print("3 - Listar ingressos de uma Sessão")
        print("0 - Voltar")
        print("-" * 30)
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n--- Venda de Ingresso ---")
            try:
                # Coleta os dados para a venda
                cliente_id = int(input("ID do Cliente: "))
                sessao_id = int(input("ID da Sessão: "))
                assento = int(input("Número do Assento: "))
                preco = float(input("Preço do Ingresso (R$): "))

                # Chama a função do módulo
                # Retornos: 0 (Sucesso), 3 (Ocupado), 1 (Não achou), 5 (Lotada), -1 (Inválido)
                codigo_retorno = Ingresso.cria_ingresso(cliente_id, sessao_id, assento, preco)
                
                # Tratamento especial para o código 5 (Sessão Lotada)
                if codigo_retorno == 5:
                    print("Erro: A sessão está LOTADA.")
                else:
                    padrao_retornos.imprime_mensagem(codigo_retorno)
                
            except ValueError:
                print("Erro: Certifique-se de digitar números válidos (Preço usa ponto, ex: 25.50).")

        elif opcao == '2':
            print("\n--- Ingressos por Cliente ---")
            try:
                id_cliente = int(input("Digite o ID do Cliente: "))
                
                # Chama a função de listagem
                lista = Ingresso.lista_ingressos_cliente(id_cliente)
                
                if not lista:
                    print("Nenhum ingresso encontrado para este cliente.")
                else:
                    print(f"Total encontrados: {len(lista)}")
                    print("-" * 60)
                    print(f"{'ID':<5} | {'Sessão':<8} | {'Assento':<8} | {'Preço'}")
                    print("-" * 60)
                    for ing in lista:
                        id_ing = ing.get('id', 'N/A')
                        id_sess = ing.get('sessao_id', 'N/A')
                        num_assento = ing.get('numero_assento', 'N/A')
                        val_preco = ing.get('preco', 0.0)
                        
                        print(f"{id_ing:<5} | {id_sess:<8} | {num_assento:<8} | R$ {val_preco:.2f}")
                    print("-" * 60)
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")

        elif opcao == '3':
            print("\n--- Ingressos por Sessão ---")
            try:
                id_sessao = int(input("Digite o ID da Sessão: "))
                
                # Chama a função de listagem
                lista = Ingresso.lista_ingressos_sessao(id_sessao)
                
                if not lista:
                    print("Nenhum ingresso vendido para esta sessão.")
                else:
                    print(f"Total vendidos: {len(lista)}")
                    print("-" * 60)
                    print(f"{'ID':<5} | {'Cliente':<8} | {'Assento':<8} | {'Preço'}")
                    print("-" * 60)
                    for ing in lista:
                        id_ing = ing.get('id', 'N/A')
                        id_cli = ing.get('cliente_id', 'N/A')
                        num_assento = ing.get('numero_assento', 'N/A')
                        val_preco = ing.get('preco', 0.0)
                        
                        print(f"{id_ing:<5} | {id_cli:<8} | {num_assento:<8} | R$ {val_preco:.2f}")
                    print("-" * 60)
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")

        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

def menu_clientes():
    while True:
        print("\n" + "-"*30)
        print("     GERENCIAR CLIENTES     ")
        print("-" * 30)
        print("1 - Cadastrar novo cliente")
        print("2 - Listar clientes")
        print("3 - Buscar cliente por ID")
        print("4 - Remover cliente")
        print("0 - Voltar")
        print("-" * 30)
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n--- Novo Cliente ---")
            nome = input("Nome completo: ").strip()
            cpf = input("CPF: ").strip()

            # Chama a função cadastra_cliente(nome, cpf)
            # Retornos esperados: 0, 2 ou -1
            codigo_retorno = Cliente.cadastra_cliente(nome, cpf)
            
            padrao_retornos.imprime_mensagem(codigo_retorno)

        elif opcao == '2':
            print("\n--- Lista de Clientes ---")
            lista = Cliente.lista_clientes()
            
            if not lista:
                print("Nenhum cliente cadastrado.")
            else:
                print(f"Total encontrados: {len(lista)}")
                print("-" * 60)
                print(f"{'ID':<5} | {'Nome':<30} | {'CPF'}")
                print("-" * 60)
                for c in lista:
                    id_c = c.get('id', 'N/A')
                    nome_c = c.get('nome', 'Sem Nome')[:30] # Corta nomes muito longos
                    cpf_c = c.get('cpf', 'N/A')
                    
                    print(f"{id_c:<5} | {nome_c:<30} | {cpf_c}")
                print("-" * 60)

        elif opcao == '3':
            print("\n--- Buscar Cliente ---")
            try:
                id_busca = int(input("Digite o ID do cliente: "))
        
                # Chama a função busca_cliente(id)
                # Retorno esperado: Dicionário ou None
                cliente_encontrado = Cliente.busca_cliente(id_busca)
                
                if cliente_encontrado:
                    print("\n" + "="*30)
                    print(f"CLIENTE #{cliente_encontrado['id']}")
                    print("="*30)
                    print(f"Nome: {cliente_encontrado['nome']}")
                    print(f"CPF:  {cliente_encontrado['cpf']}")
                    print("="*30)
                else:
                    # Se retornou None, mostramos mensagem de não encontrado
                    padrao_retornos.imprime_mensagem(padrao_retornos.NAO_ENCONTRADO)
                    
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")

        elif opcao == '4':
            print("\n--- Remover Cliente ---")
            try:
                id_remove = int(input("Digite o ID do cliente para remover: "))
                
                # Chama a função remove_cliente(id)
                # Retornos esperados: 0, 1 ou -1
                codigo_retorno = Cliente.remove_cliente(id_remove)
                
                padrao_retornos.imprime_mensagem(codigo_retorno)
                
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")

        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

def menu_sessoes():
    while True:
        print("\n" + "-"*30)
        print("     GERENCIAR SESSÕES     ")
        print("-" * 30)
        print("1 - Criar nova sessão")
        print("2 - Listar sessões")
        print("3 - Apagar sessão")
        print("4 - Buscar detalhes da sessão") 
        print("0 - Voltar")
        print("-" * 30)
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n--- Nova Sessão ---")
            try:
                # Coleta os dados (Interface com o Usuário)
                filme_id = int(input("ID do Filme: "))
                sala = int(input("Número da Sala: "))
                horario = input("Horário (HH:MM): ")
                capacidade = int(input("Capacidade da sala: "))
                formato = input("Formato (dublado/legendado): ")

                # Chama a lógica (Backend)
                codigo_retorno = Sessao.cria_sessao(filme_id, sala, horario, capacidade, formato)
                
                # Exibe o resultado usando seu padrão
                padrao_retornos.imprime_mensagem(codigo_retorno)
                
            except ValueError:
                print("Erro: Certifique-se de digitar números para ID, Sala e Capacidade.")

        elif opcao == '2':
            print("\n--- Lista de Sessões ---")
            print("Deseja filtrar a busca?")
            print("1 - Não (Listar tudo)")
            print("2 - Sim (Aplicar filtros)")
            
            escolha_filtro = input("Escolha: ")
            
            # Inicializamos os filtros como None (padrão "trazer tudo")
            f_id = None
            f_formato = None
            f_horario = None

            if escolha_filtro == '2':
                print("\n--- Configurar Filtros (Aperte ENTER para ignorar um campo) ---")
                
                # Filtro de Filme (precisa converter para int se não for vazio)
                entrada_id = input("Filtrar por ID do Filme: ").strip()
                if entrada_id: # Se tem texto (não é vazio)
                    try:
                        f_id = int(entrada_id)
                    except ValueError:
                        print("AVISO: ID inválido digitado. O filtro de filme será ignorado.")

                # Filtro de Formato (String direta)
                entrada_formato = input("Filtrar por Formato (dublado/legendado): ").strip().lower()
                if entrada_formato:
                    f_formato = entrada_formato

                # Filtro de Horário (String direta HH:MM)
                entrada_horario = input("Listar a partir de qual horário (HH:MM): ").strip()
                if entrada_horario:
                    f_horario = entrada_horario

           
            codigo, lista = Sessao.lista_sessoes(
                filtro_filme_id=f_id, 
                formato_exibicao=f_formato, 
                horario_minimo=f_horario
            )
            
            # --- EXIBIÇÃO DOS RESULTADOS ---
            if codigo == padrao_retornos.SUCESSO:
                if not lista:
                    print("\nNenhuma sessão encontrada com esses critérios.")
                else:
                    print(f"\nTotal encontradas: {len(lista)}")
                    print("-" * 60)
                    print(f"{'ID':<5} | {'Filme ID':<10} | {'Sala':<5} | {'Horário':<8} | {'Formato'}")
                    print("-" * 60)
                    for s in lista:
                        print(f"{s['id']:<5} | {s['filme_id']:<10} | {s['sala']:<5} | {s['horario']:<8} | {s['formato_exibicao']}")
                    print("-" * 60)
            else:
                padrao_retornos.imprime_mensagem(codigo)
        
        elif opcao == '3':
            print("\n--- Apagar Sessão ---")
            try:
                sessao_id = int(input("Digite o ID da sessão para apagar: "))
                
                # Chama a lógica
                codigo_retorno = Sessao.apaga_sessao(sessao_id)
                
                # Exibe resultado
                padrao_retornos.imprime_mensagem(codigo_retorno)
                
            except ValueError:
                print("Erro: O ID deve ser um número.")

        elif opcao == '4':
            print("\n--- Buscar Sessão ---")
            try:
                id_busca = int(input("Digite o ID da sessão: "))
                
                # Chama a função de busca
                sessao_encontrada = Sessao.busca_sessao(id_busca)
                
                if sessao_encontrada:
                    # Se achou, vamos buscar também os assentos disponíveis para mostrar completo
                    qtd_livres = Sessao.assentos_disponiveis(id_busca)
                    
                    print("\n" + "="*30)
                    print(f"DETALHES DA SESSÃO #{sessao_encontrada['id']}")
                    print("="*30)
                    print(f"Filme ID:   {sessao_encontrada['filme_id']}")
                    print(f"Sala:       {sessao_encontrada['sala']}")
                    print(f"Horário:    {sessao_encontrada['horario']}")
                    print(f"Formato:    {sessao_encontrada['formato_exibicao']}")
                    print("-" * 30)
                    print(f"Capacidade: {sessao_encontrada['capacidade']}")
                    print(f"Ocupados:   {len(sessao_encontrada['assentos_ocupados'])}")
                    print(f"LIVRES:     {qtd_livres}")
                    print("="*30)
                else:
                    padrao_retornos.imprime_mensagem(padrao_retornos.NAO_ENCONTRADO)
                    
            except ValueError:
                print("Erro: O ID deve ser um número.")

        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

def menu_monitoramento():
    while True:
        print("\n" + "-"*30)
        print("     RELATÓRIOS E MONITORAMENTO     ")
        print("-" * 30)
        print("1 - Receita e Ingressos de um Filme")
        print("2 - Filme Mais Assistido")
        print("3 - Receita e Ocupação de uma Sessão")
        print("4 - Total Geral de Ingressos Vendidos")
        print("0 - Voltar")
        print("-" * 30)
        
        opcao = input("Escolha uma opção: ")

        # --- Opção 1: Receita e Ingressos (Filme) ---
        if opcao == '1':
            print("\n--- Análise por Filme ---")
            try:
                id_filme = int(input("Digite o ID do Filme: "))
                
                # Chama a função do módulo
                dados = Monitoramento.receita_e_ingressos(id_filme)
                
                if dados:
                    print(f"\nResultados para o Filme ID {id_filme}:")
                    print(f"- Ingressos Vendidos: {dados['ingressos_vendidos']}")
                    print(f"- Receita Total:      R$ {dados['receita']:.2f}")
                else:
                    print("Erro: Filme não encontrado ou sem dados.")
                    
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")

        # --- Opção 2: Filme Mais Assistido ---
        elif opcao == '2':
            print("\n--- Filme Mais Assistido ---")
            

            todas_sessoes = Sessao.obtem_todas_sessoes()
            

            resultado = Monitoramento.filme_mais_assistido(todas_sessoes)
            
            if resultado:
                print(f"\nO filme mais assistido é: {resultado['titulo_filme']}")
                print(f"Total de Ingressos: {resultado['quantidade_ingressos']}")
            else:
                print("Não há dados suficientes (sessões ou ingressos) para análise.")

        # --- Opção 3: Receita e Ocupação (Sessão) ---
        elif opcao == '3':
            print("\n--- Análise por Sessão ---")
            try:
                id_sessao = int(input("Digite o ID da Sessão: "))
                
                # Chama a função
                dados = Monitoramento.receita_e_ocupacao_sessao(id_sessao)
                
                if dados:
                    print(f"\nResultados para a Sessão ID {id_sessao}:")
                    print(f"- Receita Gerada:     R$ {dados['receita']:.2f}")
                    print(f"- Taxa de Ocupação:   {dados['ocupacao_porcentagem']:.1f}%")
                else:
                    print("Erro: Sessão não encontrada.")
                    
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")

        # --- Opção 4: Total Geral de Ingressos ---
        elif opcao == '4':
            print("\n--- Contagem Global ---")
            
            # Obtém a lista de sessões novamente
            todas_sessoes = Sessao.obtem_todas_sessoes()
            
            # Chama a função
            total = Monitoramento.conta_ingressos(todas_sessoes)
            
            if total is None:
                print("Não existem sessões cadastradas.")
            elif total == -1:
                print("Erro: Parâmetros inválidos na contagem.")
            else:
                print(f"\nTotal de ingressos vendidos em TODAS as sessões: {total}")

        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

def exibe_menu_principal():
    print("\n" + "="*30)
    print("     BILHETERIA DE CINEMA     ")
    print("="*30)
    print("1 - Gerenciar FILMES")
    print("2 - Gerenciar CLIENTES")
    print("3 - Gerenciar SESSÕES")
    print("4 - Gerenciar INGRESSOS")
    print("5 - MONITORAMENTO (Relatórios)")
    print("0 - Sair")
    print("="*30)


def main():
    while True:
        exibe_menu_principal()
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n[Info] Indo para o menu de Filmes...")
            menu_filmes()
            
        elif opcao == '2':
            print("\n[Info] Indo para o menu de Clientes...")
            menu_clientes()
            
        elif opcao == '3':
            print("\n[Info] Indo para o menu de Sessões...")
            menu_sessoes()
            
        elif opcao == '4':
            print("\n[Info] Indo para o menu de Ingressos...")
            menu_ingressos()
            
        elif opcao == '5':
            print("\n[Info] Indo para o menu de Monitoramento...")
            menu_monitoramento()
            
        elif opcao == '0':
            print("\nSaindo do sistema. Até logo!")
            break
            
        else:
            print("\n[Erro] Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()