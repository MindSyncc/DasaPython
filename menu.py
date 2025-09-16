from funcoes_estoque import *
from funcoes_funcionario import *
from funcoes_consumo import *
import time
import threading

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

        match opcao:
            case '1':
                funcionario = realizar_login()
                if funcionario and funcionario['cargo'].lower() == 'administrador':
                    menu_administrador()
                else:
                    print("Acesso negado.")
                    input("Pressione Enter para continuar...")
            case '2':
                funcionario = realizar_login()
                if funcionario and funcionario['cargo'].lower() == 'funcionario':
                    menu_funcionario()
                else:
                    print("Acesso negado.")
                    input("Pressione Enter para continuar...")
            case '3':
                print("Saindo do sistema...")
                time.sleep(1)
                break
            case _:
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
        print("2. Listar Funcionários")
        print("3. Buscar Funcionário por Nome")
        print("4. Checar Estoque")
        print("5. Buscar Produto no Estoque")
        print("6. Situação do Estoque")
        print("7. Consumo diário (em desenvolvimento)")
        print("8. Sair")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case '1':
                cadastrar_funcionario()
            case '2':
                listar_funcionarios()
            case '3':
                nome = input("Digite o nome do funcionário que deseja buscar: ").strip()
                funcionario = achar_funcionario_por_nome(nome)
                if funcionario != -1:
                    print(f"Funcionário encontrado: ID: {funcionario['id']}, Nome: {funcionario['nome']}, Cargo: {funcionario['cargo']}, Data de Admissão: {funcionario['data_admissao']}")
                else:
                    print("Funcionário não encontrado.")
                input("Pressione Enter para continuar...")
            case '4':
                carregar_estoque()
            case '5':
                buscar_produto_estoque()
            case '6':
                situacao_estoque()
                input("Pressione Enter para continuar...")
            case '7':
                print("Funcionalidade em desenvolvimento.")
            case '8':
                print("Saindo do menu administrador...")
                time.sleep(1)
                break
            case _:
                print("Opção inválida.")
                input("Pressione Enter para continuar...")


def menu_funcionario() -> None:
    '''Menu do funcionário, permitindo checar e atualizar o estoque.'''
    while True:
        limpar_tela()
        atualizar_situacao_estoque()
        print("=" * 40)
        print("         MENU DO FUNCIONÁRIO")
        print("=" * 40)
        print("1. Checar Estoque")
        print("2. Adicionar Produto")
        print("3. Remover Produto")
        print("4. Sair")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case '1':
                carregar_estoque()
            case '2':
                try:
                    categoria, produto = escolher_produto()
                    quantidade = int(input("Digite a quantidade a ser adicionada: ").strip())
                    if quantidade <= 0:
                        raise ValueError
                    atualizar_estoque(categoria, produto, quantidade, "adicionar", datetime.now().strftime("%d/%m/%Y"), aleatorio=False)
                    registro_estoque(produto, quantidade, "adicionar")
                    atualizar_situacao_estoque()
                except ValueError:
                    print("Quantidade inválida. Deve ser um número inteiro positivo.")
                    input("Pressione Enter para continuar...")
            case '3':
                try:
                    categoria, produto = escolher_produto()
                    quantidade = int(input("Digite a quantidade a ser retirada: ").strip())
                    if quantidade <= 0:
                        raise ValueError
                    atualizar_estoque(categoria, produto, quantidade, "remover", datetime.now().strftime("%d/%m/%Y"), aleatorio=False)
                    registro_estoque(produto, quantidade, "remover")   
                    atualizar_situacao_estoque()
                except ValueError:
                    print("Quantidade inválida. Deve ser um número inteiro positivo.")
                    input("Pressione Enter para continuar...")
            case '4':
                print("Saindo do menu funcionário...")
                time.sleep(1)
                break
            case _:
                print("Opção inválida.")
                input("Pressione Enter para continuar...")


if __name__ == "__main__":
    t = threading.Thread(target=registro_periodico, daemon=True)
    t.start()
    menu_geral()
