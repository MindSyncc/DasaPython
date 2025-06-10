import random
import os
import json
import time
from datetime import datetime

usuario_logado = None

def carregar_dados(arquivo: str) -> dict:
    '''Carrega os dados de um arquivo JSON e retorna um dicionário.'''
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

def salvar_dados(arquivo: str, dados: dict) -> None:
    '''Salva os dados em um arquivo JSON.'''
    try:
        with open(arquivo, 'w', encoding='utf-8') as file:
            json.dump(dados, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")

def limpar_tela() -> None:
    '''Limpa a tela do terminal.'''
    os.system('cls' if os.name == 'nt' else 'clear')

def gerar_id(dados: dict) -> str:
    '''Gera um ID único para novos registros.'''
    while True:
        id = str(random.randint(1000, 9999))
        if id not in dados:
            return id

def cadastrar_funcionario() -> None:
    '''Cadastra um novo funcionário no sistema.'''
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
            input("Pressione Enter para continuar...")
            return

    funcionarios[id] = {
        'nome': nome,
        'senha': senha,
        'cargo': cargo,
        'data_admissao': data_admissao
    }
    salvar_dados('funcionarios.json', funcionarios)
    print(f"Funcionário {nome} cadastrado com sucesso! ID: {id}")
    input("Pressione Enter para continuar...")

def realizar_login() -> dict:
    '''Realiza o login de um funcionário no sistema.'''
    funcionarios = carregar_dados('funcionarios.json')
    if not funcionarios:
        print("Nenhum funcionário cadastrado.")
        input("Pressione Enter para continuar...")
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
            time.sleep(1)
            return funcionario

    print("Nome ou senha incorretos.")
    input("Pressione Enter para continuar...")
    return None

def registro_estoque(produto: str, quantidade: int, registro: str) -> None:
    '''Registra a adição ou remoção de produtos no estoque.'''
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


def atualizar_estoque(categoria: str, item: str, quantidade: int, acao: str) -> None:
    '''Atualiza o estoque de um item em uma categoria específica.'''
    estoque = carregar_dados("estoque.json")

    if categoria in estoque.get("insumos", {}):
        if item in estoque["insumos"][categoria]:
            if acao == "adicionar":
                estoque["insumos"][categoria][item] += quantidade
                print(f"{quantidade} unidades adicionadas a '{item}' em '{categoria}'.")
            elif acao == "remover":
                if estoque["insumos"][categoria][item] >= quantidade:
                    estoque["insumos"][categoria][item] -= quantidade
                    print(f"{quantidade} unidades removidas de '{item}' em '{categoria}'.")
                else:
                    print(f"Erro: Não há {quantidade} unidades suficientes de '{item}' para remover.")
            else:
                print("Erro: Ação inválida. Use 'adicionar' ou 'remover'.")
        else:
            print(f"Erro: Item '{item}' não encontrado na categoria '{categoria}'.")
    else:
        print(f"Erro: Categoria '{categoria}' não encontrada.")

    salvar_dados("estoque.json", estoque)
    input("Pressione Enter para continuar...")

def situacao_estoque() -> None:
    '''Exibe a situação do estoque, alertando sobre itens com baixo ou alto estoque.'''
    estoque = carregar_dados('estoque.json')
    for categoria in estoque.get("insumos", {}):
        print(f"\nCategoria: {categoria}")
        for item, quantidade in estoque["insumos"][categoria].items():
            if quantidade <= 100:
                print(f" - {item}: {quantidade} unidades (ALERTA: Baixo estoque!)")
            elif quantidade >= 500:
                print(f" - {item}: {quantidade} unidades (ALERTA: Estoque alto!)")
            else:
                print(f" - {item}: {quantidade} unidades (Estoque normal)")

def atualizar_situacao_estoque() -> None:
    estoque = carregar_dados('estoque.json')
    situacao_estoque = {}

    for categoria, itens in estoque.get("insumos", {}).items():
        situacao_estoque[categoria] = {}
        for item, quantidade in itens.items():
            if quantidade <= 100:
                situacao_estoque[categoria][item] = "BAIXO"
            elif quantidade >= 500:
                situacao_estoque[categoria][item] = "ALTO"
            else:
                situacao_estoque[categoria][item] = "NORMAL"

    salvar_dados('situacao_estoque.json', situacao_estoque)

def notificacao_estoque() -> None:
    '''Notifica sobre itens com baixo estoque.'''
    estoque = carregar_dados('estoque.json')
    for categoria in estoque.get("insumos", {}):
        for item, quantidade in estoque["insumos"][categoria].items():
            if quantidade <= 100:
                print(f"ALERTA: O item '{item}' na categoria '{categoria}' está com baixo estoque ({quantidade} unidades).")

def carregar_estoque() -> None:
    '''Carrega e exibe o estoque atual.'''
    estoque = carregar_dados('estoque.json')
    if estoque and "insumos" in estoque:
        print("Estoque atual:\n")
        for categoria, itens in estoque["insumos"].items():
            print(f"[{categoria}]")
            for nome_item, quantidade in itens.items():
                print(f" - {nome_item}: {quantidade} unidades")
            print()
    else:
        print("Estoque vazio")
    input("Pressione Enter para voltar para o menu...")

def menu_geral() -> None:
    '''Menu principal do sistema de estoque. Permite acesso como administrador ou funcionário.'''
    while True:
        limpar_tela()
        print("=" * 40)
        print("      SISTEMA DE ESTOQUE - MINDSYNC")
        print("=" * 40)
        print("1. Acessar como Administrador")
        print("2. Acessar como Funcionário")
        print("3. Sair")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            funcionario = realizar_login()
            if funcionario and funcionario['cargo'].lower() == 'administrador':
                menu_administrador()
            else:
                print("Acesso negado.")
                input("Pressione Enter para continuar...")
        elif opcao == '2':
            funcionario = realizar_login()
            if funcionario and funcionario['cargo'].lower() == 'funcionario':
                menu_funcionario()
            else:
                print("Acesso negado.")
                input("Pressione Enter para continuar...")
        elif opcao == '3':
            print("Saindo do sistema...")
            time.sleep(1)
            break
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")

def menu_administrador() -> None:
    '''Menu do administrador, permitindo gerenciar funcionários e estoque.'''
    while True:
        limpar_tela()
        atualizar_situacao_estoque()
        notificacao_estoque()
        print("=" * 40)
        print("         MENU DO ADMINISTRADOR")
        print("=" * 40)
        print("1. Cadastrar Funcionário")
        print("2. Checar Estoque")
        print("3. Situação do Estoque")
        print("4. Sair")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()
        if opcao == '1':
            cadastrar_funcionario()
        elif opcao == '2':
            carregar_estoque()
        elif opcao == '3':
            situacao_estoque()
            input("Pressione Enter para continuar...")
        elif opcao == '4':
            print("Saindo do menu administrador...")
            time.sleep(1)
            break
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")

def menu_funcionario() -> None:
    '''Menu do funcionário, permitindo checar e atualizar o estoque.'''
    while True:
        limpar_tela()
        atualizar_situacao_estoque()
        notificacao_estoque()
        print("=" * 40)
        print("         MENU DO FUNCIONÁRIO")
        print("=" * 40)
        print("1. Checar Estoque")
        print("2. Adicionar Produto")
        print("3. Remover Produto")
        print("4. Sair")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()
        if opcao == '1':
            carregar_estoque()
        elif opcao == '2':
            try:
                categoria = input("Digite a categoria do produto: ").strip()
                produto = input("Digite o nome do produto: ").strip()
                quantidade = int(input("Digite a quantidade a ser adicionada: ").strip())
                if quantidade <= 0:
                    raise ValueError
                atualizar_estoque(categoria, produto, quantidade, "adicionar")
                registro_estoque(produto, quantidade, "adicionar")
                atualizar_situacao_estoque()
            except ValueError:
                print("Quantidade inválida. Deve ser um número inteiro positivo.")
                input("Pressione Enter para continuar...")
        elif opcao == '3':
            try:
                categoria = input("Digite a categoria do produto: ").strip()
                produto = input("Digite o nome do produto: ").strip()
                quantidade = int(input("Digite a quantidade a ser retirada: ").strip())
                if quantidade <= 0:
                    raise ValueError
                atualizar_estoque(categoria, produto, quantidade, "remover")
                registro_estoque(produto, quantidade, "remover")
                atualizar_situacao_estoque()
            except ValueError:
                print("Quantidade inválida. Deve ser um número inteiro positivo.")
                input("Pressione Enter para continuar...")
        elif opcao == '4':
            print("Saindo do menu funcionário...")
            time.sleep(1)
            break
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    menu_geral()
