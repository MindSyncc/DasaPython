# Sistema de Controle de Estoque e Consumo Diário - DASA

## 👥 Grupo MindSync

**Integrantes:**
- Juan Fuentes Rufino - RM557673 - 2ESPV
- Pedro Henrique Silva Batista - RM558137 - 2ESPV
- Heloísa Fleury Jardim - RM556378 - 2ESPV
- Fernando Carlos Colque Huaranca - RM558095 - 2ESPI
- Julia Carolina Ferreira Silva - RM558896 - 2ESPI

------------------------------------------------------------------------

## 📋 Introdução

Este projeto é um sistema de controle de estoque e consumo diário de
insumos desenvolvido para a **Sprint 3 do Challenge 2025 - 2º Semestre
da FIAP** em parceria com a **DASA**.

O sistema simula o gerenciamento de insumos médicos em uma unidade de
coleta de exames, permitindo o registro de entradas e saídas, controle
de consumo diário e geração de relatórios.

Foi desenvolvido em **Python** com armazenamento em **arquivos JSON**,
implementando diversas estruturas de dados e algoritmos conforme exigido
na Sprint 3, incluindo **filas**, **pilhas**, **busca sequencial e
binária**, e **algoritmos de ordenação**.

Nessa nova versão do algoritmo, ele também implementa funções que calculam 
o gasto com o estoque e previsão na solicitação do estoque. Essas funções 
tiveram o objetivo de acelerar o uso do algoritmo e adicionar funcionali-
dades que são necessárias para a empresa DASA.

------------------------------------------------------------------------

## 🚀 Funcionalidades

-   **Gestão de Estoque**: Controle completo de insumos por categorias
    (coleta de sangue, urina, fezes e materiais gerais)
-   **Registro de Consumo Diário**: Armazenamento dos consumos dos
    últimos 7 dias
-   **Sistema de Login**: Dois níveis de acesso (Administrador e
    Funcionário)
-   **Geração Automática de Dados**: Registros aleatórios de consumo
    para simulação
-   **Relatórios e Alertas**: Notificações de estoque baixo e alto
-   **Busca Eficiente**: Implementação de busca binária e sequencial
-   **Ordenação**: Algoritmo **Merge Sort** para organização dos dados
-   **Otimização com Programação Dinâmica**: Previsão de demanda e
recomendações de reposição otimizadas.
------------------------------------------------------------------------

## 🛠️ Tecnologias Utilizadas

-   **Python 3.8+**
-   **JSON** para armazenamento de dados
-   **Faker** para geração de dados aleatórios
-   **Threading** para execução de processos em paralelo

------------------------------------------------------------------------

## 📦 Instalação e Execução

### Pré-requisitos

-   Python 3.8 ou superior instalado
-   Gerenciador de pacotes `pip`

### Passos para instalação

Clone ou baixe os arquivos do projeto:

``` bash
git clone <URL_DO_REPOSITORIO>
```

Instale as dependências:

``` bash
pip install faker
```

Execute o sistema:

``` bash
python menu.py
```

### Logins de teste

-   **Administrador**: usuário: `teste`, senha: `teste`
-   **Funcionário**: usuário: `teste1`, senha: `teste1`

------------------------------------------------------------------------

## 🎯 Como Usar o Sistema

### Menu Principal

Ao executar o sistema, você terá acesso ao menu principal com três
opções:
1. Acessar como Administrador
2. Acessar como Funcionário
3. Sair

### Funcionalidades do Administrador

-   Cadastrar novos funcionários
-   Listar todos os funcionários
-   Buscar funcionário por nome (busca sequencial)
-   Checar estoque completo
-   Buscar produto no estoque (busca binária)
-   Ver situação do estoque (alertas de baixo/alto estoque)
-   Otimização com Programação Dinâmica: Recomendações inteligentes de reposição
### Funcionalidades do Funcionário

-   Checar estoque
-   Adicionar produtos ao estoque
-   Remover produtos do estoque (registrando consumo)

------------------------------------------------------------------------

## ⚙️ Geração Automática de Dados

O sistema possui uma **thread em segundo plano** que gera registros
aleatórios de consumo a cada 5 segundos, incluindo:
- Datas aleatórias dos últimos 7 dias
- Produtos selecionados aleatoriamente
- Quantidades aleatórias entre 100-500 unidades
- Tipo de registro (adicionar/remover) baseado no estoque atual
- 

------------------------------------------------------------------------

## 📊 Estruturas de Dados Implementadas

### 1️⃣ Fila (Consumo Diário)

O sistema implementa uma fila **FIFO (First-In, First-Out)** para
gerenciar o consumo diário, mantendo apenas os registros dos últimos 7
dias:

``` python
def consumo_diario_limpar(dados_consumo: dict, limite: int = 7) -> None:
    '''Limitar o uso do arquivo consumo_diario.json para os últimos 7 dias.'''
    if "consumo_diario" in dados_consumo:
        fila_consumo = dados_consumo["consumo_diario"]
        while len(fila_consumo) > limite: #FIFO
            fila_consumo.pop(0) # Remove o registro mais antigo
```

### 2️⃣ Busca Sequencial e Binária

**Busca Binária (Complexidade: O(log n))**

``` python
def busca_binaria(lista, alvo):
    '''Realiza uma busca binária em uma lista ordenada.'''
    esquerda, direita = 0, len(lista) - 1
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        if lista[meio] == alvo:
            return meio
        elif lista[meio] < alvo:
            esquerda = meio + 1
        else:
            direita = meio - 1
    return -1
```

**Busca Sequencial (Complexidade: O(n))**

``` python
def busca_sequencial(lista, alvo):
    '''Realiza uma busca sequencial em uma lista.'''
    for i in range(len(lista)):
        if lista[i] == alvo:
            return i
    return -1
```

### 3️⃣ Algoritmos de Ordenação

**Merge Sort (Complexidade: O(n log n))**

``` python
def merge_sort(lista):
    '''Ordena uma lista usando o algoritmo merge sort.'''
    if len(lista) <= 1:
        return lista
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio])
    direita = merge_sort(lista[meio:])
    resultado = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        if esquerda[i] < direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1
    while j < len(direita):
        resultado.append(direita[j])
        j += 1
    return resultado
```

### 4️⃣ Programação Dinâmica - Otimização de Estoque
O sistema implementa três versões de Programação Dinâmica para otimizar as decisões de reposição de estoque:

**Formulação do Problema**
    - Estados: (dia, estoque_atual)
    - Decisões: Quantidade a pedir a cada dia
    - Função de Transição: novo_estoque = estoque_atual - demanda[dia] + pedido

**Função Objetivo**: 
    - Minimizar custo total (pedido + estoque + falta)
    
   Versão Recursiva (Top-Down)
python

    def dp_recursiva_estoque(dia, estoque_atual, demanda, custo_pedido=50.0, ...):
        """Abordagem Top-Down pura - explora todas as possibilidades"""
        # Caso base
        if dia >= len(demanda):
            return 0, 0
    
        # Calcular custos do dia atual
        # Explorar decisões de pedido
        # Chamada recursiva para próximo estado
**Versão com Memorização**
python

    def dp_memorizacao_estoque(dia, estoque_atual, demanda, ...):
        """Otimização com cache - evita recálculos desnecessários"""
        global MEMO_DP
        chave = (dia, estoque_atual)
        if chave in MEMO_DP:
            return MEMO_DP[chave]  
        # Mesma lógica da recursiva, mas com cache
        MEMO_DP[chave] = resultado
        return resultado
**Versão Iterativa (Bottom-Up)**
python

    def dp_iterativa_estoque(demanda, estoque_inicial=0, ...):
        """Abordagem Bottom-Up - preenche tabela DP iterativamente"""
        # Inicializar tabelas DP
        dp = [[float('inf')] * (capacidade_max + 1) for _ in range(n_dias + 1)]
        
        # Preencher de trás para frente
        for dia in range(n_dias - 1, -1, -1):
            for estoque in range(capacidade_max + 1):
                # Calcular melhor decisão para cada estado
**Verificação de Consistência**
python

    def verificar_consistencia_dp(demanda):
        """Garante que todas as versões produzem os mesmos resultados"""
        # Testa as três versões e compara resultados
        # Retorna True se custos forem consistentes
###
------------------------------------------------------------------------

## 📁 Estrutura de Arquivos

``` text
sistema_estoque/
├── consumo_diario.json      # Registros de consumo dos últimos 7 dias
├── estoque.json            # Estoque atual de todos os insumos
├── funcionarios.json       # Cadastro de funcionários
├── registros.json          # Histórico completo de movimentações
├── situacao_estoque.json   # Status de cada item (baixo/normal/alto)
├── recomendacoes_reposicao.json   # Recomendações de reposição de cada item
├── teste_programacao_dinamica.py   # Teste para ver se os métodos de otimização batem
├── funcoes_dinaimcas_lucro.py   # Funções de programação dinâmica voltadas a maximizar o lucro
├── menu.py                 # Menu principal do sistema
├── funcoes_consumo.py      # Funções relacionadas ao consumo
├── funcoes_estoque.py      # Funções de gestão de estoque
├── funcoes_funcionario.py  # Funções de gestão de funcionários
├── funcoes_gerais.py       # Funções auxiliares e algoritmos
└── README.md               # Este arquivo
```

------------------------------------------------------------------------

## ✅ Requisitos Atendidos (Sprint 3)

### Diagrama de Casos de Uso

O sistema implementa todos os casos de uso essenciais:
- Login de usuários (Administrador e Funcionário)
- Gestão de funcionários (apenas Administrador)
- Consulta de estoque
- Registro de entrada/saída de insumos
- Geração de relatórios de consumo

### Backlog do Produto

Todas as funcionalidades prioritárias foram implementadas:
- Sistema de autenticação com dois níveis de acesso
- Controle de estoque com categorias específicas
- Registro de movimentações (entrada/saída)
- Alertas de estoque baixo e alto
- Geração de relatórios de consumo
- Interface de linha de comando intuitiva

### Estruturas de Dados e Algoritmos

-   **Fila**: Gestão do consumo diário (últimos 7 dias)
-   **Busca Sequencial**: Para encontrar funcionários por nome
-   **Busca Binária**: Para localizar produtos no estoque
-   **Merge Sort**: Para ordenação de insumos por prioridade
-   **Programação Dinâmica**: Geração de registros aleatórios com base
    no estado atual do estoque

### Protótipo

O sistema oferece uma **interface de linha de comando completa e
intuitiva**, com menus hierárquicos e feedback visual para todas as
operações.

## ✅ Requisitos Atendidos (Sprint 4)

### - **Bottom-Up**:
- **Onde**: `dp_iterativa_estoque()` em `funcoes_dinamicas_lucro.py`
- **O que faz**: Calcula recomendações de reposição otimizadas construindo solução iterativamente dos menores para os maiores subproblemas

### - **Top-Down com Memorização**:
- **Onde**: `dp_memorizacao_estoque()` em `funcoes_dinamicas_lucro.py`
- **O que faz**: Resolve o problema de estoque recursivamente com cache para evitar recálculos, partindo do problema principal

###  - **Recursiva**:
- **Onde**: `dp_recursiva_estoque()` em `funcoes_dinamicas_lucro.py`
- **O que faz**: Implementação recursiva pura que explora todas as possibilidades de decisão de pedidos

### **Verificação de Consistência**:
- **Onde**: `verificar_consistencia_dp()` em `funcoes_dinamicas_lucro.py`
- **O que faz**: Garante que todas as três versões de Programação Dinâmica produzam os mesmos resultados para validação
    
------------------------------------------------------------------------

## 📈 Exemplos de Uso

### Consultando um produto no estoque:

1.  Acesse como Administrador ou Funcionário
2.  Selecione "Buscar Produto no Estoque"
3.  Digite o nome do produto (ex: "agulhas")
4.  O sistema retornará a categoria e quantidade disponível

### Adicionando produtos ao estoque:

1.  Acesse como Funcionário
2.  Selecione "Adicionar Produto"
3.  Escolha a categoria e o produto
4.  Informe a quantidade a ser adicionada
5.  O sistema atualizará o estoque e registrará a movimentação

### Verificando alertas de estoque:

-   Acesse como Administrador
-   O sistema exibirá automaticamente alertas de itens com estoque
    **baixo (\<100 unidades)** ou **alto (\>500 unidades)**

------------------------------------------------------------------------

## 📈 Funções de teste programação dinâmica

### Otimizando reposição com Programação Dinâmica:
1.   Acesse como Administrador
2.   Selecione "Programação Dinâmica - Otimização de Estoque"
3.   Escolha "Otimizar reposição de todos os insumos"
4.   O sistema analisará o consumo histórico e recomendará:
       Quantidades ideais para pedir
       Custos mínimos projetados
       Sequência de reposição para 7 dias



