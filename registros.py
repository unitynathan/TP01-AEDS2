from aluno import Aluno
from bloco import Bloco

def organizar_em_blocos(lista_alunos, tamanho_bloco, modo, espalhamento=False):
   
    # função principal que organiza os registros de alunos em blocos de acordo com a estratégia escolhida.
    
    if modo == 1: # tamanho Fixo
        return _organizar_tamanho_fixo(lista_alunos, tamanho_bloco)
    elif modo == 2: # tamanho Variável
        if espalhamento:
            return _organizar_variavel_espalhado(lista_alunos, tamanho_bloco)
        else:
            return _organizar_variavel_contiguo(lista_alunos, tamanho_bloco)

def _organizar_tamanho_fixo(lista_alunos, tamanho_bloco):
    blocos = [Bloco(id_bloco=1, tamanho_maximo=tamanho_bloco)]
    
    for aluno in lista_alunos:
        registro_bytes = aluno.to_bytes_fixo()
        
        bloco_atual = blocos[-1]
        if bloco_atual.espaco_livre() < len(registro_bytes):
            # se não cabe, cria um novo bloco
            bloco_atual = Bloco(id_bloco=len(blocos) + 1, tamanho_maximo=tamanho_bloco)
            blocos.append(bloco_atual)
            
        bloco_atual.adicionar_dados(registro_bytes)
        
    return blocos

def _organizar_variavel_contiguo(lista_alunos, tamanho_bloco):
    blocos = [Bloco(id_bloco=1, tamanho_maximo=tamanho_bloco)]

    for aluno in lista_alunos:
        registro_bytes = aluno.to_bytes_variavel()
        
        bloco_atual = blocos[-1]
        if bloco_atual.espaco_livre() < len(registro_bytes):
            # se não cabe, então move o registro inteiro para o próximo bloco livre
            bloco_atual = Bloco(id_bloco=len(blocos) + 1, tamanho_maximo=tamanho_bloco)
            blocos.append(bloco_atual)

        bloco_atual.adicionar_dados(registro_bytes)

    return blocos

def _organizar_variavel_espalhado(lista_alunos, tamanho_bloco):
    blocos = [Bloco(id_bloco=1, tamanho_maximo=tamanho_bloco)]
    
    for aluno in lista_alunos:
        registro_bytes = aluno.to_bytes_variavel()
        bytes_restantes = len(registro_bytes)
        bytes_escritos = 0

        while bytes_restantes > 0:
            bloco_atual = blocos[-1]
            espaco = bloco_atual.espaco_livre()

            if espaco == 0:
                # se o bloco atual está cheio, cria um novo
                bloco_atual = Bloco(id_bloco=len(blocos) + 1, tamanho_maximo=tamanho_bloco)
                blocos.append(bloco_atual)
                espaco = bloco_atual.espaco_livre()

                # pega a parte do registro que cabe no bloco atual
            parte_para_escrever = registro_bytes[bytes_escritos : bytes_escritos + espaco]
            bloco_atual.adicionar_dados(parte_para_escrever)
            
            bytes_escritos += len(parte_para_escrever)
            bytes_restantes -= len(parte_para_escrever)
            
    return blocos

def escrever_arquivo_dat(blocos, nome_arquivo="alunos.dat"):
    """Concatena os dados de todos os blocos e escreve no arquivo .dat."""
    with open(nome_arquivo, 'wb') as f:
        for bloco in blocos:
            # preenche o restante do bloco com um byte de preenchimento, para que todos os blocos tenham o mesmo tamanho.
            dados_completos = bloco.dados.ljust(bloco.tamanho_maximo, b'\0')
            f.write(dados_completos)