import gerar
import registros
import utils
from gerenciador import GerenciadorArmazenamento

def main():
    print("--- Simulador de Armazenamento (TP01 + TP02) ---")
    
    # 1. Configurações iniciais
    num_alunos = int(input("Quantidade de alunos para gerar inicialmente: "))
    tamanho_bloco = int(input("Tamanho do bloco em bytes: "))
    modo = int(input("Modo (1: Fixo, 2: Variável): "))
    
    espalhamento = False
    if modo == 2:
        espalhamento = input("Permitir espalhamento? (s/n): ").lower() == 's'

    # 2. GERAÇÃO (Aqui é onde o nome deve bater!)
    print(f"\nGerando {num_alunos} registros...")
    
    # IMPORTANTE: Definimos 'lista_inicial' aqui
    lista_inicial = gerar.gerar_lista_alunos(num_alunos) 
    
    # 3. ORGANIZAÇÃO (Agora o Python vai encontrar a 'lista_inicial')
    blocos = registros.organizar_em_blocos(lista_inicial, tamanho_bloco, modo, espalhamento)
    
    # Cria o gerenciador com as regras escolhidas
    gerente = GerenciadorArmazenamento(blocos, modo, espalhamento, tamanho_bloco)
    
    # --- PARTE DO TP02: Menu de Operações ---
    while True:
        print("\n--- MENU DE MANUTENÇÃO ---")
        print("1. Inserir Novo Aluno")
        print("2. Excluir Aluno (Lógico)")
        print("3. Editar Aluno")
        print("4. Reorganizar (Compactar)")
        print("5. Ver Status do Disco")
        print("6. Ver Lista de registros")
        print("0. Sair e Salvar")
        
        op = input("Escolha: ")
        
        if op == '1':
            print("\n--- Inserindo Novo Aluno ---")
            # Para facilitar, vamos gerar um aleatório, mas mostrar os dados
            novo = gerar.gerar_lista_alunos(1)[0]
            print(f"Gerado: {novo.nome} (Matrícula: {novo.matricula})")
            
            if gerente.inserir_aluno(novo):
                print(">>> Sucesso: Aluno inserido e salvo.")
            input("\nPressione Enter para voltar ao menu...")

        elif op == '2':
            print("\n--- Exclusão Lógica de Aluno ---")
            try:
                mat = int(input("Digite a matrícula para excluir: "))
                
                # Chama o gerenciador e verifica o retorno
                if gerente.excluir_aluno(mat):
                    print(f"\n[OK] Registro {mat} marcado como EXCLUÍDO com sucesso.")
                    print("O espaço agora está disponível para reaproveitamento.")
                else:
                    print(f"\n[ERRO] Aluno com matrícula {mat} não foi encontrado.")
            
            except ValueError:
                print("\n[ERRO] Por favor, digite um número de matrícula válido.")
            
            # ESTA LINHA É A MAIS IMPORTANTE: ela faz o programa parar para você ler
            input("\nPressione Enter para voltar ao menu...")

        elif op == '3':
            print("\n--- Editando Aluno ---")
            mat_busca = int(input("Digite a matrícula do aluno que deseja editar: "))
            
            # Criamos um objeto com os novos dados (ex: novo nome)
            print("Digite os novos dados (simulação de edição):")
            novo_nome = input(f"Novo nome para o aluno {mat_busca}: ")
            
            # Geramos um aluno "modelo" com o nome novo para passar ao gerente
            aluno_editado = gerar.gerar_lista_alunos(1)[0]
            aluno_editado.matricula = mat_busca
            aluno_editado.nome = novo_nome
            
            if gerente.editar_aluno(mat_busca, aluno_editado):
                print(">>> Sucesso: Aluno editado.")
            else:
                print(">>> Erro: Aluno não encontrado.")
            input("\nPressione Enter para voltar ao menu...")
            
        elif op == '4':
            print("\nIniciando Reorganização Física...")
            
            # 1. Tira uma "foto" de como o arquivo está agora (cheio de buracos)
            antes = utils.calcular_metricas(gerente.blocos)
            
            # 2. Executa a limpeza (gera a nova lista de blocos)
            gerente.blocos = gerente.reorganizar()
            
            # 3. Tira uma "foto" de como ficou depois (compactado)
            depois = utils.calcular_metricas(gerente.blocos)
            
            # 4. CHAMA A EXIBIÇÃO do relatório que estava faltando
            utils.exibir_comparativo(antes, depois)
            
            # 5. SALVA o novo arquivo compactado (como pede o manual)
            registros.escrever_arquivo_dat(gerente.blocos, "alunos_reorg.dat")
            print("\n[AVISO] Novo arquivo 'alunos_reorg.dat' gerado com sucesso.")
            
            # 6. PAUSA para você conseguir ler os dados antes do menu voltar
            input("\nPressione Enter para continuar...")
            
        elif op == '5':
            utils.exibir_estatisticas(gerente.blocos)
            
        elif op == '6':
            print("\n" + "="*60)
            print(f"{'BLOCO':<6} | {'STATUS':<8} | {'MATRÍCULA':<10} | {'NOME'}")
            print("-" * 60)
            
            total_ativos = 0
            for bloco in gerente.blocos:
                registros_no_bloco = 0
                for offset, status, tam, mat in bloco.percorrer_registros():
                    registros_no_bloco += 1
                    if status == 'A':
                        nome = bloco.obter_nome_registro(offset)
                        print(f"{bloco.id:<6} | {'Ativo':<8} | {mat:<10} | {nome}")
                        total_ativos += 1
                    else:
                        print(f"{bloco.id:<6} | {'Excluído':<8} | {mat:<10} | --------")
                
                if registros_no_bloco == 0:
                    print(f"{bloco.id:<6} | (Bloco Vazio ou Corrompido)")

            print("-" * 60)
            print(f"Total de registros ativos encontrados: {total_ativos}")
            print("="*60)
            input("\nPressione Enter para continuar...")
            
        elif op == '0':
            registros.escrever_arquivo_dat(gerente.blocos)
            break

if __name__ == "__main__":
    main()