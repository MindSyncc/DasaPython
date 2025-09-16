import re
from datetime import datetime
from funcoes_gerais import *
import time

def cadastrar_funcionario() -> None:
    '''Cadastra um novo funcionário no sistema.'''
    funcionarios = carregar_dados('funcionarios.json')
    try:
        nome = input("Digite o nome do funcionário: ").strip()
        if not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", nome):
            print("Erro: O nome deve conter apenas letras e espaços.")
            input("Pressione Enter para continuar...")
        senha = input("Digite a senha do funcionário: ").strip()
        if not re.fullmatch(r"[A-Za-z0-9@#$%^&+=]{6,}", senha):
            print("Erro: A senha deve ter pelo menos 6 caracteres e pode conter letras, números e símbolos (@#$%^&+=).")
            input("Pressione Enter para continuar...")
            return
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


def listar_funcionarios() -> None:
    '''Lista todos os funcionários cadastrados no sistema.'''
    funcionarios = carregar_dados('funcionarios.json')
    if not funcionarios:
        print("Nenhum funcionário cadastrado.")
    else:
        print("Funcionários cadastrados:")
        for id, info in funcionarios.items():
            print(f"""ID: {id}
                  Nome: {info['nome']} 
                  Cargo: {info['cargo']}
                  Data de Admissão: {info['data_admissao']}""")
    input("Pressione Enter para continuar...")


def achar_funcionario_por_nome(nome: str) -> dict:
    '''Busca um funcionário pelo nome usando busca sequencial.'''
    funcionarios = carregar_dados("funcionarios.json") or {}
    lista_funcionarios = []
    for chave, dados in funcionarios.items():
        dados_com_id = {"id": chave}
        dados_com_id.update(dados)
        lista_funcionarios.append(dados_com_id)

    # Buscar pelo nome usando busca sequencial
    return busca_sequencial(lista_funcionarios, nome)


def realizar_login() -> dict:
    '''Realiza o login de um funcionário no sistema.'''
    funcionarios = carregar_dados('funcionarios.json')
    if not funcionarios:
        print("Nenhum funcionário cadastrado.")
        time.sleep(1)
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
    time.sleep(1)
    return None