import struct

class Aluno:
    def __init__(self, matricula, nome, cpf, curso, filiacao_mae, filiacao_pai, ano_ingresso, ca, status='A'):
        self.matricula = int(matricula)
        self.nome = nome
        self.cpf = cpf
        self.curso = curso
        self.filiacao_mae = filiacao_mae
        self.filiacao_pai = filiacao_pai
        self.ano_ingresso = int(ano_ingresso)
        self.ca = float(ca)
        self.status = status # 'A' para Ativo, 'E' para Excluído

    def _gerar_corpo_fixo(self):
        """Gera os bytes no formato fixo (160 bytes de dados)."""
        return struct.pack('<I 50s 11s 30s 30s 30s I f', 
            self.matricula, 
            self.nome.encode('utf-8')[:50].ljust(50, b'\0'),
            self.cpf.encode('utf-8')[:11].ljust(11, b'\0'),
            self.curso.encode('utf-8')[:30].ljust(30, b'\0'),
            self.filiacao_mae.encode('utf-8')[:30].ljust(30, b'\0'),
            self.filiacao_pai.encode('utf-8')[:30].ljust(30, b'\0'),
            self.ano_ingresso, 
            self.ca
        )

    def _gerar_corpo_variavel(self):
        """Gera os bytes no formato variável."""
        dados_fixos = struct.pack('<I I f', self.matricula, self.ano_ingresso, self.ca)
        dados_vars = b''
        for campo in [self.nome, self.cpf, self.curso, self.filiacao_mae, self.filiacao_pai]:
            b_campo = campo.encode('utf-8')
            dados_vars += struct.pack('<B', len(b_campo)) + b_campo
        return dados_fixos + dados_vars

    def to_bytes_fixo(self):
        """Método que o registros.py procura para modo FIXO."""
        corpo = self._gerar_corpo_fixo()
        header = struct.pack('<c H', self.status.encode('ascii'), len(corpo) + 3)
        return header + corpo

    def to_bytes_variavel(self):
        """Método que o registros.py procura para modo VARIÁVEL (Corrige seu erro)."""
        corpo = self._gerar_corpo_variavel()
        header = struct.pack('<c H', self.status.encode('ascii'), len(corpo) + 3)
        return header + corpo

    def get_bytes(self, modo):
        """Método auxiliar para o Gerenciador usar o modo correto."""
        return self.to_bytes_fixo() if modo == 1 else self.to_bytes_variavel()

    def __repr__(self):
        return f"Aluno(mat={self.matricula}, nome='{self.nome}')"