import struct

class Bloco:
    def __init__(self, id_bloco, tamanho_maximo):
        self.id = id_bloco
        self.tamanho_maximo = tamanho_maximo
        self.dados = bytearray(b'')

    def espaco_livre(self):
        return self.tamanho_maximo - len(self.dados)

    @property
    def ocupacao(self):
        return len(self.dados)

    @property
    def percentual_ocupacao(self):
        if self.tamanho_maximo == 0: return 0
        return (self.ocupacao / self.tamanho_maximo) * 100

    def percorrer_registros(self):
        offset = 0
        # Enquanto houver espaço para pelo menos o Header (3 bytes) + Matrícula (4 bytes)
        while offset + 7 <= len(self.dados):
            try:
                # 1. Lê o Status e o Tamanho do Registro
                status_byte, tam_registro = struct.unpack_from('<c H', self.dados, offset)
                status = status_byte.decode('ascii')

                # 2. Segurança: Se o tamanho for 0 ou maior que o bloco, algo está errado
                if tam_registro == 0 or tam_registro > self.tamanho_maximo:
                    break 

                # 3. Lê a Matrícula (está após o Header de 3 bytes)
                matricula = struct.unpack_from('<I', self.dados, offset + 3)[0]

                yield (offset, status, tam_registro, matricula)
                
                # 4. Pula para o próximo registro
                offset += tam_registro
            except:
                # Se der erro em um registro, para de ler este bloco
                break

    def marcar_excluido(self, matricula_alvo):
        for offset, status, tam, mat in self.percorrer_registros():
            if mat == matricula_alvo and status == 'A':
                self.dados[offset] = ord('E') # Muda 'A' para 'E'
                return True
        return False
    
    def obter_nome_registro(self, offset):
        """
        Navega nos bytes para extrair o nome.
        Pulo: Header(3) + Matrícula(4) + Ingresso(4) + CA(4) = 15 bytes.
        """
        try:
            # O byte 15 (a partir do offset) guarda o tamanho do nome
            posicao_tam_nome = offset + 15
            tam_nome = self.dados[posicao_tam_nome]
            
            # Os bytes seguintes são o texto
            inicio_nome = posicao_tam_nome + 1
            fim_nome = inicio_nome + tam_nome
            nome_bytes = self.dados[inicio_nome : fim_nome]
            
            return nome_bytes.decode('utf-8')
        except:
            return "Nome não identificado"