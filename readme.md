Sistema de Controle de Estoque - DASA (Simulação)

INTEGRANTES:
Fernando Carlos Colque Huaranca - rm558095

Heloísa Fleury Jardim - rm556378 - 2ESPV

Juan Fuentes Rufino - rm557673

Julia Carolina Ferreira Silva - rm558896

Pedro Batista - rm558137

 Sobre o Projeto
Este projeto simula o controle de estoque de uma unidade da DASA (Diagnósticos da América), voltada para a coleta de sangue, urina e fezes. Diante de problemas reais de controle e comunicação interna enfrentados por laboratórios, esta solução foi idealizada para oferecer um sistema simples, funcional e com atualizações em tempo real do estoque.

O objetivo é melhorar a visibilidade e gestão de insumos críticos usados no processo de coleta, garantindo que não faltem itens essenciais nem haja desperdício por excesso.

 Como Funciona
O sistema é executado via terminal (CLI - Command Line Interface), simulando dois tipos de usuários:

Administrador: pode cadastrar funcionários e consultar a situação do estoque.

Funcionário: pode registrar movimentações (entrada/saída) e consultar produtos.

#Logins testes
Login do administrador:
usuario: teste
senha: teste

Login do Usuario:
usuario: teste1
usuario: teste1

As informações são armazenadas em arquivos JSON, simulando um banco de dados simples, e os dados do estoque são atualizados em tempo real após cada ação.

 Funcionalidades
 Acesso
Login com usuário e senha

Dois perfis de acesso: administrador e funcionário

🛒 Estoque
Registro de entrada e saída de insumos

Controle por categoria (ex: "tubos", "luvas", "etiquetas")

Situação do estoque (baixo, normal ou alto)

Notificações para itens com estoque crítico

Busca binária para localizar rapidamente um item (eficiente com grandes volumes)

 Administração
Cadastro de novos funcionários

Registro com nome, senha, cargo e data de admissão

Proteção contra duplicidade de funcionários

 Estrutura de Arquivos
estoque.json: contém os insumos categorizados com suas quantidades

funcionarios.json: armazena os usuários cadastrados

registros.json: histórico de movimentações no estoque

situacao_estoque.json: status atual de cada item (baixo, normal, alto)

 Hipóteses e Dados Considerados
Categorias como: tubos, luvas, seringas, frascos, etiquetas, etc.

Um estoque com variação entre 0 a 1000 unidades por item

Faixas de alerta:

🔴 Abaixo de 100 unidades: Baixo estoque

🟢 Acima de 500 unidades: Estoque alto

Todos os insumos são identificados por nome (string) e quantidade (inteiro)

A entrada/saída é controlada manualmente por funcionários

O sistema não está integrado com sensores nem bancos de dados externos

 Estrutura Técnica

 Algoritmos Aplicados
Busca Binária (O(log n)) para localizar itens rapidamente no estoque

Ordenação (O(n log n)) antes da busca para garantir eficiência

Análises de Complexidade (O-grande) documentadas nas funções principais

(Opcional) Recursividade com memorização pode ser adicionada para fins didáticos

Armazenamento
Todos os dados são salvos em arquivos JSON

A leitura/escrita é feita de forma segura e com tratamento de erros

 Normas e Boas Práticas
Código documentado com docstrings em cada função

Nomes de variáveis descritivos e em português

Separação clara entre lógica de negócios e interface do usuário (menu)

Comentários com análise de complexidade onde necessário



Como Executar

Certifique-se de ter o Python instalado (3.8+)

Clone o projeto ou copie os arquivos .py e .json


Siga as instruções no terminal

🧪 Exemplo de Uso
Funcionário acessa o sistema

Escolhe “Adicionar Produto”

Digita: categoria = tubos, produto = tubo roxo, quantidade = 200

Produto é registrado e estoque atualizado

Se quantidade cair abaixo de 100, um alerta será exibido ao administrador

Login do administrador:
usuario: teste
senha: teste

Login do Usuario:
usuario: teste1
usuario: teste1