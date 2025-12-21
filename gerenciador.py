import struct
from bloco import Bloco

class GerenciadorArmazenamento:
    def __init__(self, blocos, modo, espalhamento, tamanho_padrao):
        # Agora o Gerenciador aceita todos os parâmetros do seu main.py
        self.blocos = blocos
        self.modo = modo               # 1: Fixo, 2: Variável
        self.espalhamento = espalhamento # True ou False
        self.tamanho_padrao = tamanho_padrao

    def inserir_aluno(self, novo_aluno):
        """Insere um aluno respeitando o modo (Fixo/Var) e o reuso de espaço."""
        # Pega os bytes no formato correto (Fixo ou Variável)
        dados_novos = novo_aluno.get_bytes(self.modo)
        tam_novo = len(dados_novos)

        # 1. Tenta Reutilizar Espaço (First-Fit em registros excluídos 'E')
        # Nota: Só funciona bem para registros NÃO-ESPALHADOS
        for bloco in self.blocos:
            for offset, status, tam_existente, mat in bloco.percorrer_registros():
                if status == 'E' and tam_existente >= tam_novo:
                    bloco.dados[offset : offset + tam_novo] = dados_novos
                    return True

        # 2. Tenta adicionar ao final de um bloco que tenha espaço
        for bloco in self.blocos:
            if bloco.espaco_livre() >= tam_novo:
                bloco.dados.extend(dados_novos)
                return True

        # 3. Se não coube em nenhum, cria bloco novo
        novo_id = len(self.blocos) + 1
        novo_bloco = Bloco(novo_id, self.tamanho_padrao)
        novo_bloco.dados.extend(dados_novos)
        self.blocos.append(novo_bloco)
        return True

    def reorganizar(self):
        """Executa a compactação física do arquivo."""
        registros_ativos = []

        # 1. Coleta apenas o que não foi excluído
        for bloco in self.blocos:
            for offset, status, tam, mat in bloco.percorrer_registros():
                if status == 'A':
                    # Extrai os bytes exatos do registro ativo
                    bytes_registro = bloco.dados[offset : offset + tam]
                    registros_ativos.append(bytes_registro)
        
        # 2. Reconstrói os blocos do zero, de forma densa
        novos_blocos = [Bloco(1, self.tamanho_padrao)]
        
        for reg in registros_ativos:
            # Se não cabe no bloco atual, cria o próximo
            if novos_blocos[-1].espaco_livre() < len(reg):
                novo_id = len(novos_blocos) + 1
                novos_blocos.append(Bloco(novo_id, self.tamanho_padrao))
            
            novos_blocos[-1].dados.extend(reg)
            
        return novos_blocos
    
    def editar_aluno(self, matricula_alvo, aluno_novo):
        for bloco in self.blocos:
            for offset, status, tam_antigo, mat in bloco.percorrer_registros():
                if mat == matricula_alvo and status == 'A':
                    # Pega o nome antigo para confirmação
                    nome_antigo = bloco.obter_nome_registro(offset)
                    
                    dados_novos = aluno_novo.get_bytes(self.modo)
                    if len(dados_novos) <= tam_antigo:
                        bloco.dados[offset : offset + len(dados_novos)] = dados_novos
                    else:
                        bloco.dados[offset] = ord('E') # Exclui o antigo
                        self.inserir_aluno(aluno_novo) # Insere o novo em outro lugar
                    
                    return nome_antigo # Retorna o nome que foi alterado
        return None
    
    def excluir_aluno(self, matricula):
        """Procura o aluno em todos os blocos e marca como excluído."""
        for bloco in self.blocos:
            if bloco.marcar_excluido(matricula):
                return True # Retorna True assim que encontrar e excluir
        return False # Retorna False se percorrer tudo e não achar