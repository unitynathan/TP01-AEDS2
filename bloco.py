
class Bloco:
    def __init__(self, id_bloco, tamanho_maximo):
        self.id = id_bloco
        self.tamanho_maximo = tamanho_maximo
        self.dados = b''                                        # Conteúdo do bloco em bytes

    def espaco_livre(self):
       
        return self.tamanho_maximo - len(self.dados)            # Retorna quantidade de bytes livres no bloco

    def adicionar_dados(self, novos_dados):
        
        if len(novos_dados) <= self.espaco_livre():             # Adiciona uma sequência de bytes ao bloco. Retorna verdadeiro se bem sucedido
            self.dados += novos_dados
            return True
        return False

    @property
    def ocupacao(self):
        
        return len(self.dados)                                  # Retorna o número de bytes ocupados
    
    @property
    def percentual_ocupacao(self):
       
        if self.tamanho_maximo == 0:                             # Retorna o percentual de ocupação do bloco
            return 0
        return (self.ocupacao / self.tamanho_maximo) * 100

    def __repr__(self):
        return f"Bloco {self.id}: {self.ocupacao}/{self.tamanho_maximo} bytes ({self.percentual_ocupacao:.2f}%)"