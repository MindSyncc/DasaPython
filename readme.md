📋 Sistema de Controle de Estoque - DASA
📖 Visão Geral
Sistema de controle de estoque desenvolvido para laboratórios DASA (Diagnósticos da América), especializado no gerenciamento de insumos médicos para coleta de materiais biológicos. A solução oferece controle em tempo real do estoque com alertas inteligentes para situações críticas.

🎯 Objetivo
Melhorar a gestão de insumos médicos essenciais, prevenindo tanto a falta quanto o excesso de produtos através de um sistema eficiente com atualizações em tempo real.

👥 Equipe
Fernando Carlos Colque Huaranca - rm558095

Heloísa Fleury Jardim - rm556378 - 2ESPV

Juan Fuentes Rufino - rm557673

Julia Carolina Ferreira Silva - rm558896

Pedro Batista - rm558137

⚙️ Funcionalidades
🔐 Sistema de Autenticação
Login com usuário e senha

Dois perfis de acesso: Administrador e Funcionário

Controle de permissões por cargo

📦 Gestão de Estoque
✅ Registro de entrada e saída de insumos

✅ Controle por categorias organizadas

✅ Sistema de alertas para estoque baixo/alto

✅ Busca eficiente de produtos

✅ Histórico completo de movimentações

👥 Administração
✅ Cadastro de novos funcionários

✅ Controle de acesso hierárquico

✅ Prevenção contra duplicidade de registros

📊 Relatórios e Monitoramento
✅ Situação do estoque em tempo real

✅ Consumo diário de insumos

✅ Notificações automáticas

🏗️ Arquitetura do Sistema
📋 Estrutura de Arquivos
text
sistema_estoque/
├── menu.py                 # Menu principal do sistema
├── funcoes_gerais.py       # Funções utilitárias gerais
├── funcoes_estoque.py      # Funções de gestão de estoque
├── funcoes_funcionario.py  # Funções de gestão de usuários
├── funcoes_consumo.py      # Funções de controle de consumo
├── estoque.json           # Dados de estoque atual
├── funcionarios.json      # Base de usuários cadastrados
├── registros.json         # Histórico de movimentações
├── consumo_diario.json    # Registro de consumo por data
└── situacao_estoque.json  # Status atual dos itens
🧮 Algoritmos Implementados
Algoritmo	Complexidade	Localização	Status
Busca Binária	O(log n)	funcoes_gerais.py	✅ Implementado
Busca Sequencial	O(n)	funcoes_gerais.py	✅ Implementado
Merge Sort	O(n log n)	funcoes_gerais.py	✅ Implementado
Fila (FIFO)	O(1) para remoção	funcoes_consumo.py	✅ Implementado
🚀 Como Executar
Pré-requisitos
Python 3.8 ou superior instalado

Bibliotecas: Faker (instalável via pip)

Instalação
bash
# Clone o repositório ou copie os arquivos
git clone <repositorio>

# Instale as dependências (se necessário)
pip install faker

# Execute o sistema
python menu.py
🔐 Credenciais de Acesso
Administrador:

Usuário: teste

Senha: teste

Funcionário:

Usuário: teste1

Senha: teste1

📋 Categorias de Produtos
🩸 Coleta de Sangue
Agulhas, Gazes, Seringas, Algodão, Tubos de Transporte

💧 Coleta de Urina
Frascos Estéreis, Frascos de Urina 24h, Copos Coletores

💩 Coleta de Fezes
Frascos Coletores, Espátulas Descartáveis, Sacos Plásticos

🧼 Materiais Gerais
Máscaras Cirúrgicas, Propé, Toucas Descartáveis, Sabonete Líquido, Papel Toalha, Etiquetas Identificadoras, Luvas Descartáveis

⚠️ Sistema de Alertas
🔴 Estoque Baixo: Abaixo de 100 unidades

🟢 Estoque Alto: Acima de 500 unidades

🟡 Estoque Normal: Entre 100 e 500 unidades

🔄 Fluxo de Trabalho
Login → Autenticação no sistema

Menu Principal → Acesso conforme perfil

Gestão de Estoque → Adição/remoção de itens

Registro Automático → Histórico de movimentações

Atualização em Tempo Real → Situação do estoque

Alertas → Notificações de estoque crítico

📊 Exemplo de Uso
python
# 1. Login como funcionário
# 2. Navegar até "Adicionar Produto"
# 3. Selecionar categoria: "coleta_sangue"
# 4. Selecionar produto: "agulhas"
# 5. Informar quantidade: 200
# 6. Sistema atualiza estoque automaticamente
# 7. Registro é salvo no histórico
🛠️ Tecnologias Utilizadas
Linguagem: Python 3.8+

Armazenamento: JSON files

Interface: CLI (Command Line Interface)

Autenticação: Sistema próprio de usuários/senhas

Data e Hora: Biblioteca datetime nativa

📈 Status do Projeto
✅ Funcionalidades Implementadas
Sistema de autenticação com dois perfis

CRUD completo de estoque

Sistema de alertas de estoque

Histórico de movimentações

Busca binária e sequencial

Algoritmo de ordenação Merge Sort

Estrutura de dados Fila (FIFO)

Consumo diário com limite automático

Interface intuitiva em português

📋 Requisitos Pendentes
Implementação de Quick Sort

Implementação de estrutura de Pilha

Melhorias na documentação de funções

Sistema de backup automático

Relatórios estatísticos avançados

🐛 Solução de Problemas
Erro Comum: Módulo não encontrado
bash
# Instale o Faker se necessário
pip install faker
Erro Comum: Arquivo JSON corrompido
Verifique se os arquivos JSON estão com formatação válida

Execute o sistema novamente para regenerar arquivos se necessário

📞 Suporte
Para dúvidas técnicas ou problemas de implementação, entre em contato com a equipe de desenvolvimento através dos emails institucionais.

📄 Licença
Este projeto é destinado para fins educacionais como parte do curso de Ciência da Computação.