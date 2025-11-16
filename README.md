# TP01-AEDS2

Trabalho prático desenvolvido na disciplina **Algoritmos e Estruturas de Dados II**, com foco na **simulação de armazenamento de registros em arquivos binários**.  
O projeto explora diferentes estratégias de organização dos dados (tamanho fixo e variável), avaliando a eficiência de ocupação dos blocos e gerando estatísticas sobre o uso do espaço.

---

## Estrutura do Projeto

- `aluno.py` → Classe e métodos relacionados ao objeto **Aluno**  
- `alunos.dat` → Arquivo binário com registros simulados  
- `bloco.py` → Implementação da estrutura de **blocos de armazenamento**  
- `gerar.py` → Script para gerar registros de teste  
- `main.py` → Ponto de entrada principal do programa  
- `registros.py` → Manipulação de registros 
- `utils.py` → Funções auxiliares para manipulação de dados  

---

## Como executar

### 1. Clonar o repositório
```bash
git clone https://github.com/unitynathan/TP01-AEDS2.git
cd TP01-AEDS2
```

### 2. Instalar bilioteca Faker
```bash
pip install faker
```

### 3. Executar o programa principal
Ao executar, o .DAT é gerado no decorrer da execução do programa.
```bash
python main.py

```

### 4. Funcionalidades
- Simulação de armazenamento em arquivos binários

- Organização de registros em blocos de tamanho fixo e tamanho variável

- Estatísticas de ocupação e eficiência do espaço

### 5. Exemplo de uso
```bash
python main.py

Saída esperada (exemplo simplificado):
Bloco 1: 80% ocupado
Bloco 2: 65% ocupado
Eficiência total: 72%

```