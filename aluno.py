import struct

class Aluno:
    FORMATO_FIXO = '<I 50s 11s 30s 30s 30s I f'
    TAMANHO_REGISTRO_FIXO = struct.calcsize(FORMATO_FIXO)
    
    def __init__(self, matricula, nome, cpf, curso, filiacao_mae, filiacao_pai, ano_ingresso, ca):
        self.matricula = int(matricula)
        self.nome = nome
        self.cpf = cpf
        self.curso = curso
        self.filiacao_mae = filiacao_mae
        self.filiacao_pai = filiacao_pai
        self.ano_ingresso = int(ano_ingresso)
        self.ca = float(ca)

    def to_bytes_fixo(self):
        
        return struct.pack(
            self.FORMATO_FIXO,
            self.matricula,
            self.nome.encode('utf-8').ljust(50, b'\0'),
            self.cpf.encode('utf-8').ljust(11, b'\0'),
            self.curso.encode('utf-8').ljust(30, b'\0'),
            self.filiacao_mae.encode('utf-8').ljust(30, b'\0'),
            self.filiacao_pai.encode('utf-8').ljust(30, b'\0'),
            self.ano_ingresso,
            self.ca
        )

    def to_bytes_variavel(self):
        
        dados_fixos = struct.pack('<I I f', self.matricula, self.ano_ingresso, self.ca)
        
        nome_bytes = self.nome.encode('utf-8')
        curso_bytes = self.curso.encode('utf-8')
        mae_bytes = self.filiacao_mae.encode('utf-8')
        pai_bytes = self.filiacao_pai.encode('utf-8')
        cpf_bytes = self.cpf.encode('utf-8')

        dados_variaveis = b''
        dados_variaveis += struct.pack('<B', len(nome_bytes)) + nome_bytes
        dados_variaveis += struct.pack('<B', len(curso_bytes)) + curso_bytes
        dados_variaveis += struct.pack('<B', len(mae_bytes)) + mae_bytes
        dados_variaveis += struct.pack('<B', len(pai_bytes)) + pai_bytes
        dados_variaveis += struct.pack('<B', len(cpf_bytes)) + cpf_bytes
        
        return dados_fixos + dados_variaveis

    def __repr__(self):
        """Representação em string do objeto, útil para debug."""
        return f"Aluno(mat={self.matricula}, nome='{self.nome}')"
