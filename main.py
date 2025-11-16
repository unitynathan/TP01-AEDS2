import utils
import gerar
import registros

def main():
    print("Simulador de Armazenamento de Registros")
    
    #Geração de dados
    num_alunos = int(input("Digite o número de registros de alunos a serem gerados: "))
    lista_alunos = gerar.gerar_lista_alunos(num_alunos)
    print(f"{len(lista_alunos)} registros de alunos gerados.")

    #Definição dos parâmetros
    tamanho_bloco = 0
    while tamanho_bloco < 163:
        tamanho_bloco = int(input("Digite o tamanho máximo do bloco (em bytes): "))
        if tamanho_bloco < 163:
            print("Não é possível gerar um bloco com tamanho menor comparado ao tamanho do maior registro do arquivo")
            print("Por favor insira um novo valor para o bloco que seja maior que 163 bytes")

    modo = int(input("Escolha o modo de armazenamento (1: Fixo, 2: Variável): "))
    
    espalhamento = False

    if modo == 2:
        escolha_espalhamento = input("Permitir espalhamento de registros entre blocos? (s/n): ")
        espalhamento = escolha_espalhamento.lower() == 's'

    #Simulação de escrita (organização em blocos)
    blocos_resultantes = registros.organizar_em_blocos(
        lista_alunos, tamanho_bloco, modo, espalhamento
    )
    
    #Gravação em arquivo
    registros.escrever_arquivo_dat(blocos_resultantes)
    print(f"Arquivo 'alunos.dat' gerado com sucesso.")

    #Exibição dos resultados
    utils.exibir_estatisticas(blocos_resultantes)

if __name__ == "__main__":
    main()