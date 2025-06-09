import random
import os
import json
from datetime import datetime
# Estrutura inicial do estoque
'''
Projeto desenvolvido pela MindSync
Membros:
Juan Fuentes Rufino
Pedro Henrique Silva Batista
Heloisa Fleury Jardins
Fernando Carlos Colque Huaranca
Julia Silva
'''
global login_usuario
login_usuario = False

def carregar_dados(arquivo: json) -> dict:
    ''' Carrega os dados do estoque de um arquivo.'''
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as file:
            try:
                conteudo = file.read().strip() # Lê o conteúdo do arquivo
                if not conteudo: # Verifica se o conteúdo está vazio
                    return {} #Arquivo vazio, retorna dicionário vazio
                return json.loads(conteudo)  # Converte o conteúdo JSON em um dicionário
            except json.JSONDecodeError:
                print("Erro ao decodificar o arquivo JSON. Verifique o formato.")
                return {}
    return {}


def salvar_dados(arquivo: json, dados: dict):
    ''' Salva os dados do estoque em um arquivo.'''
    with open(arquivo, 'w', encoding='utf-8') as file:
        json.dump(dados, file, ensure_ascii=False, indent=4)  # Salva o dicionário como JSON formatado


def gerar_id(dados: dict) -> str:
    ''' Gera um ID aleatório entre 1000 e 9999.'''
    id = random.randint(1000, 9999)
    while id in dados:
        id = random.randint(1000, 9999)
    return id


def cadastrar_funcionario() -> None:
    ''' Função para cadastrar um usuário.'''
    funcionarios = carregar_dados('funcionarios.json')
    nome = input("Digite o nome do funcionário: ")
    senha = input("Digite o email do funcionário: ")
    cargo = "funcionário"
    id = gerar_id(funcionarios)
    data_admissao = datetime.now().strftime("%d/%m/%Y")
    
    for user in funcionarios.values():
        if user['nome'] == nome:
            print("Funcionário já cadastrado.")
            return
    funcionarios[id] = {
        'nome': nome,
        'senha': senha,
        'cargo': cargo,
        'data_admissao': data_admissao
    }
    salvar_dados('funcionarios.json', funcionarios)
    print(f"Funcionário {nome} cadastrado com sucesso! ID: {id}")

def login_usuario() -> None:
    ''' Função para realizar o login de um usuário.'''
    global login_usuario
    funcionarios = carregar_dados('funcionarios.json')
    if not login_usuario: 
        nome = input("Digite seu nome: ")
        senha = input("Digite sua senha: ")
        if not funcionarios:
            print("Nenhum funcionário cadastrado. Por favor, cadastre um funcionário primeiro.")
            return
        for funcionario in funcionarios.values():
            if funcionario['nome'] == nome and funcionario['senha'] == senha:
                login_usuario = True
                print(f"Login realizado com sucesso! Bem-vindo, {nome}.")
                return
    else:
        print("Você já está logado.")
        return

def menu_geral():
    '''Exibe o primeiro menu do sistema.'''
    while True:
        print("\nMenu Principal:")
        print("1. Acessar como Administrador")
        print("2. Acessar como Funcionário")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            funcionario = login_usuario()
            if funcionario['cargo'] == 'ADMINISTRADOR':
                menu_administrador()
            else:
                print("Você não tem permissão para acessar o menu de administrador.")
        elif opcao == '2':
            funcionario = login_usuario()
            if funcionario['cargo'] == 'FUNCIONARIO':
                menu_funcionario()
            
        elif opcao == '3':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")   
def menu_administrador():
    ''' Exibe o menu principal do sistema enquanto administrador.'''
    while True:
        print("\nMenu Principal:")
        print("1. Cadastrar Funcionário")
        print("2. Checar estoque")
        print("3. Notifições do estoque")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")
        match opcao:
            case '1':
                cadastrar_funcionario()
            case '2':
                estoque = carregar_dados('estoque.json')
                if estoque:
                    print("Estoque atual:")
                    for id, produto in estoque.items():
                        print(f"ID: {id}, Produto: {produto['nome']}, Quantidade: {produto['quantidade']}")
                else:
                    print("Estoque vazio.")
            case '3':
                print("Notificações do estoque ainda não implementadas.")
            case '4':
                print("Saindo do sistema...")
                break
            case _:
                print("Opção inválida. Tente novamente.")
        
def menu_funcionario():
    ''' Exibe o menu principal do sistema enquanto funcionário.'''
    while True:
        print("\nMenu Principal:")
        print("1. Checar estoque")
        print("2. Adcionar produto ao estoque")
        print("3. Retirar produto do estoque")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")
        match opcao:
            case '1':
                print("Checando estoque...")
            case '2':
                print("Adicionando produto ao estoque...")
            case '3':
                print("Retirando produto do estoque...")
            case '4':
                print("Saindo do sistema...")
                break
            case _:
                print("Opção inválida. Tente novamente.")




    

