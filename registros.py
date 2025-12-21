import struct
from bloco import Bloco

def organizar_em_blocos(lista_alunos, tamanho_bloco, modo, espalhamento=False):
    """Encaminha para a estratégia escolhida pelo usuário."""
    if modo == 1:
        return _organizar_tamanho_fixo(lista_alunos, tamanho_bloco)
    elif modo == 2:
        if espalhamento:
            return _organizar_variavel_espalhado(lista_alunos, tamanho_bloco)
        else:
            return _organizar_variavel_contiguo(lista_alunos, tamanho_bloco)

def _organizar_tamanho_fixo(lista_alunos, tamanho_bloco):
    """Estratégia: Registros de tamanho fixo (Unspanned)."""
    blocos = [Bloco(id_bloco=1, tamanho_maximo=tamanho_bloco)]
    for aluno in lista_alunos:
        reg_bytes = aluno.to_bytes_fixo()
        if blocos[-1].espaco_livre() < len(reg_bytes):
            blocos.append(Bloco(id_bloco=len(blocos) + 1, tamanho_maximo=tamanho_bloco))
        blocos[-1].dados.extend(reg_bytes)
    return blocos

def _organizar_variavel_contiguo(lista_alunos, tamanho_bloco):
    """Estratégia: Registros variáveis sem quebra entre blocos (Unspanned)."""
    blocos = [Bloco(id_bloco=1, tamanho_maximo=tamanho_bloco)]
    for aluno in lista_alunos:
        reg_bytes = aluno.to_bytes_variavel()
        if blocos[-1].espaco_livre() < len(reg_bytes):
            blocos.append(Bloco(id_bloco=len(blocos) + 1, tamanho_maximo=tamanho_bloco))
        blocos[-1].dados.extend(reg_bytes)
    return blocos

def _organizar_variavel_espalhado(lista_alunos, tamanho_bloco):
    """Estratégia: Registros variáveis que podem ser divididos (Spanned)."""
    blocos = [Bloco(id_bloco=1, tamanho_maximo=tamanho_bloco)]
    for aluno in lista_alunos:
        reg_bytes = aluno.to_bytes_variavel()
        bytes_restantes = len(reg_bytes)
        bytes_escritos = 0

        while bytes_restantes > 0:
            bloco_atual = blocos[-1]
            espaco_disponivel = bloco_atual.espaco_livre()

            if espaco_disponivel == 0:
                bloco_atual = Bloco(id_bloco=len(blocos) + 1, tamanho_maximo=tamanho_bloco)
                blocos.append(bloco_atual)
                espaco_disponivel = bloco_atual.espaco_livre()

            # Pega apenas o que cabe no bloco atual
            parte = reg_bytes[bytes_escritos : bytes_escritos + espaco_disponivel]
            bloco_atual.dados.extend(parte)
            
            bytes_escritos += len(parte)
            bytes_restantes -= len(parte)
    return blocos

def escrever_arquivo_dat(blocos, nome_arquivo="alunos.dat"):
    """Grava fisicamente no disco preenchendo blocos incompletos com zeros."""
    with open(nome_arquivo, 'wb') as f:
        for bloco in blocos:
            dados_completos = bloco.dados.ljust(bloco.tamanho_maximo, b'\0')
            f.write(dados_completos)