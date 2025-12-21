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






# TP02-AEDS2 

## Simulador de Armazenamento de Registros (TP01 + TP02)

Este projeto foi desenvolvido para a disciplina de **Algoritmos e Estruturas de Dados II**. Ele consiste em um motor de armazenamento que simula como bancos de dados gerenciam registros em arquivos binários, utilizando conceitos de blocos, fragmentação e manutenção dinâmica.

---

## 🛠️ Evolução do Projeto (TP02)

Diferente da primeira versão (estática), este sistema agora suporta operações dinâmicas de manutenção:

- **Cabeçalhos de Registro (Headers):** Cada registro possui metadados (3 bytes) indicando o status (`'A'` para Ativo, `'E'` para Excluído) e seu tamanho total.
- **Exclusão Lógica:** Implementação de remoção sem custo imediato de I/O, marcando registros para futuro reaproveitamento.
- **Edição com Realocação:** Suporte a registros de tamanho variável. Se um registro editado crescer, o sistema o realoca para um novo espaço, mantendo a integridade.
- **Compactação (Reorganização):** Função de "Vacuum" que elimina a fragmentação externa e interna, reduzindo o número de blocos no disco.

---

## 📁 Estrutura de Arquivos

| Arquivo | Função |
| :--- | :--- |
| `main.py` | Ponto de entrada e interface do menu interativo. |
| `gerenciador.py` | Lógica de CRUD (Inserção, Exclusão, Edição e Reorganização). |
| `aluno.py` | Definição da classe Aluno e serialização binária (Fixo/Variável). |
| `bloco.py` | Gerenciamento da estrutura física dos blocos de memória. |
| `registros.py` | Funções de organização inicial e persistência em `.dat`. |
| `utils.py` | Cálculos de métricas, eficiência e relatórios de estatísticas. |
| `gerar.py` | Gerador de dados aleatórios utilizando a biblioteca **Faker**. |

---

## 🚀 Como Executar

### 1. Requisitos
Certifique-se de ter o Python 3 instalado e a biblioteca `faker`:
```bash
pip install faker

2. Rodando o Simulador
python main.py
```
## Conceitos de Armazenamento Implementados

Estratégias de Organização
Tamanho Fixo: Registros com slots padronizados. Rápido, mas gera fragmentação interna.

Tamanho Variável: Registros ocupam apenas o necessário. Economiza espaço, mas exige gerenciamento de headers.

Espalhamento (Spanned): Capacidade de dividir um registro entre dois blocos (opcional na configuração inicial).

Relatório de Eficiência
O sistema calcula a eficiência baseada no espaço útil (registros ativos) versus o tamanho total ocupado no arquivo físico, permitindo visualizar o ganho após a Reorganização.

## Exemplo de Uso (Menu)

Configuração Inicial: Define-se o modo de arquivo e gera-se a massa de dados.

Manutenção: Insira ou exclua alunos para ver os "buracos" surgirem no mapa de ocupação.

Reorganização: Execute a opção 4 para compactar o arquivo e gerar o relatório de ganho de eficiência.