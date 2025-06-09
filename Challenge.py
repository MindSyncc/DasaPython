import random
import os
import json
from datetime import datetime

'''
Projeto desenvolvido pela MindSync
Membros:
Juan Fuentes Rufino
Pedro Henrique Silva Batista
Heloisa Fleury Jardins
Fernando Carlos Colque Huaranca
Julia Silva
'''

# Variável global para controle de login
usuario_logado = None

def carregar_dados(arquivo: str) -> dict:
    ''' Carrega os dados do estoque de um arquivo. '''
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as file:
            try:
                conteudo = file.read().strip()
                if not conteudo:
                    return {}
                return json.loads(conteudo)
            except json.JSONDecodeError:
                print("Erro ao decodificar o arquivo JSON. Verifique o formato.")
                return {}
    return {}


def salvar_dados(arquivo: str, dados: dict):
    ''' Salva os dados em um arquivo JSON formatado. '''
    try:
        with open(arquivo, 'w', encoding='utf-8') as file:
            json.dump(dados, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")


def limpar_tela():
    ''' Limpa a tela do terminal. '''
    os.system('cls' if os.name == 'nt' else 'clear')


def gerar_id(dados: dict) -> str:
    ''' Gera um ID único entre 1000 e 9999. '''
    while True:
        id = str(random.randint(1000, 9999))
        if id not in dados:
            return id

def cadastrar_funcionario() -> None:
    ''' Cadastra um novo funcionário. '''
    funcionarios = carregar_dados('funcionarios.json')
    try:
        nome = input("Digite o nome do funcionário: ").strip()
        senha = input("Digite a senha do funcionário: ").strip()
    except Exception as e:
        print(f"Erro na entrada de dados: {e}")
        return
    
    cargo = "funcionario"
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

def realizar_login() -> dict:
    ''' Realiza login e retorna o dicionário do usuário logado. '''
    funcionarios = carregar_dados('funcionarios.json')
    if not funcionarios:
        print("Nenhum funcionário cadastrado.")
        return None

    try:
        nome = input("Digite seu nome: ").strip()
        senha = input("Digite sua senha: ").strip()
    except Exception as e:
        print(f"Erro na entrada: {e}")
        return None

    for funcionario in funcionarios.values():
        if funcionario['nome'] == nome and funcionario['senha'] == senha:
            print(f"Login realizado com sucesso! Bem-vindo, {nome}.")
            return funcionario

    print("Nome ou senha incorretos.")
    return None

def registro_estoque(produto: str, quantidade: int, registro: str) -> None:
    ''' Registra a adição ou remoção de produtos no estoque. '''
    registros = carregar_dados('registros.json')
    id = gerar_id(registros)
    data_registro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    registros[id] = {
        'insumo': produto,
        'quantidade': quantidade,
        'data_registro': data_registro,
        'tipo_registro': registro
    }
    salvar_dados('registros.json', registros)
    print(f"Produto {produto} registrado com sucesso! ID: {id}")


def atualizar_estoque_insumos(nome_categoria: str, nome_produto: str, quantidade: int, acao: str):
    ''' Atualiza o estoque de insumos agrupado por categorias e produtos. '''
    dados = carregar_dados('estoque.json')
    estoque = dados.get("insumos", {})

    if nome_categoria not in estoque:
        print(f"Categoria '{nome_categoria}' não encontrada.")
        return

    categoria = estoque[nome_categoria]
    if nome_produto not in categoria:
        if acao == "adicionar":
            categoria[nome_produto] = [quantidade]
            print(f"Produto '{nome_produto}' criado na categoria '{nome_categoria}' com {quantidade} unidades.")
        else:
            print(f"Produto '{nome_produto}' não encontrado na categoria '{nome_categoria}'.")
            return
    else:
        if acao == "adicionar":
            categoria[nome_produto][-1] += quantidade
            print(f"Adicionado {quantidade} unidades ao produto '{nome_produto}' na categoria '{nome_categoria}'.")
        elif acao == "remover":
            if categoria[nome_produto][-1] < quantidade:
                print(f"Estoque insuficiente para remover {quantidade} unidades de '{nome_produto}'.")
                return
            categoria[nome_produto][-1] -= quantidade
            print(f"Removido {quantidade} unidades do produto '{nome_produto}' na categoria '{nome_categoria}'.")
        else:
            print("Ação inválida. Use 'adicionar' ou 'remover'.")
            return

    dados["insumos"][nome_categoria] = categoria
    salvar_dados('estoque.json', dados)

    registro_estoque(nome_produto, quantidade, acao)


def menu_geral():
    ''' Exibe o menu principal do sistema. '''
    while True:
        print("\nMenu Principal:")
        print("1. Acessar como Administrador")
        print("2. Acessar como Funcionário")
        print("3. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            funcionario = realizar_login()
            if funcionario:
                if funcionario['cargo'].lower() == 'administrador':
                    menu_administrador()
                else:
                    print("Você não tem permissão para acessar o menu de administrador.")
        elif opcao == '2':
            funcionario = realizar_login()
            if funcionario:
                if funcionario['cargo'].lower() == 'funcionario':
                    menu_funcionario()
                else:
                    print("Você não é um funcionário.")
        elif opcao == '3':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_administrador():
    ''' Menu exclusivo para administradores. '''
    while True:
        limpar_tela()
        print("\nMenu Administrador:")
        print("1. Cadastrar Funcionário")
        print("2. Checar estoque")
        print("3. Notificações do estoque")
        print("4. Sair")

        opcao = input("Escolha uma opção: ").strip()
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
                print("Saindo do menu administrador...")
                break
            case _:
                print("Opção inválida. Tente novamente.")

def menu_funcionario():
    limpar_tela()
    ''' Menu para funcionários. '''
    while True:
        print("\nMenu Funcionário:")
        print("1. Checar estoque")
        print("2. Adicionar produto ao estoque")
        print("3. Retirar produto do estoque")
        print("4. Sair")

        opcao = input("Escolha uma opção: ").strip()
        match opcao:
            case '1':
                estoque = carregar_dados('estoque.json')
                if estoque:
                    print("Estoque atual:")
                    for id, produto in estoque.items():
                        print(f"ID: {id}, Produto: {produto['nome']}, Quantidade: {produto['quantidade']}")
                else:
                    print("Estoque vazio.")
            case '2':
                try:
                    produto = input("Digite o nome do produto: ").strip()
                    quantidade = int(input("Digite a quantidade a ser adicionada: ").strip())
                    registro_estoque(produto, quantidade, 'adicionar')
                    atualizar_estoque_insumos("Insumos", produto, quantidade, "adicionar")
                except ValueError:
                    print("Quantidade inválida. Deve ser um número inteiro.")
                
                if quantidade <= 0:
                    print("Quantidade deve ser maior que zero.")
                    continue
                
                registro_estoque(produto, quantidade, 'adicionar')
            case '3':
                try:
                    produto = input("Digite o nome do produto: ").strip()
                    quantidade = int(input("Digite a quantidade a ser retirada: ").strip())
                    registro_estoque(produto, quantidade, 'remover')
                    atualizar_estoque_insumos("Insumos", produto, quantidade, "remover")
                except ValueError:
                    produto = input("Digite o nome do produto: ").strip()
                    quantidade = int(input("Digite a quantidade a ser retirada: ").strip())
                
                if quantidade <= 0:
                    print("Quantidade deve ser maior que zero.")
                    continue
            case '4':
                print("Saindo do menu funcionário...")
                break
            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_geral()
