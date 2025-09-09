from datetime import datetime
import re
import time
from funcoes_gerais import *

def organizar_insumos_por_consumo() -> dict:
    '''Organiza os insumos do estoque com base no último consumo registrado'''
    #Carrega os dados
    estoque = carregar_dados('estoque.json')
    registros = carregar_dados('registro.json')

    #Encontra o último registro de consumo (remover)
    consumos = [
        valor for valor in registros.values()
        if valor.get("tipo_registro") == "remover"
    ]
    
    if not consumos:
        return estoque  # nenhum consumo registrado ainda

    #Encontra o consumo mais recente na lista 'consumos'
    #A função 'max' vai comparar os itens da lista e retornar o maior segundo o critério definido em 'key'
    ultimo_consumo = max(
        consumos,  # Lista de dicionários, cada um representando um consumo
        key=lambda x: datetime.strptime(
            x["data_registro"],  #Acessa a string da data dentro do dicionário
            "%d/%m/%Y %H:%M:%S"  #Define o formato da data para conversão
        )
    )
    insumo_consumido = ultimo_consumo["insumo"]

    #Cria a lista [(insumo, quantidade, prioridade)]
    lista_insumos = []
    for categoria, itens in estoque["insumos"].items():
        for nome, qtd in itens.items():
            prioridade = 0 if nome == insumo_consumido else 1
            lista_insumos.append((nome, qtd, prioridade))

    #Ordena a lista por quick_sort
        lista_ordenada = quick_sort(lista_insumos, key=lambda x: (x[2], x[0]))
    #Reconstrui dicionário ordenado
    insumos_ordenados = {nome: qtd for nome, qtd, _ in lista_ordenada}

    return insumos_ordenados


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
    return busca_sequencial(lista_funcionarios, "nome", nome)


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


def escolher_produto() -> tuple[str, str]:
    '''Permite ao usuário escolher um produto e retorna (categoria, item) com nomes compatíveis com o JSON.'''    
    categorias = {
        1: ("coleta_sangue", {
            1: ("Agulhas", "agulhas"),
            2: ("Gazes", "gazes"),
            3: ("Seringas", "seringas"),
            4: ("Algodão", "algodao"),
            5: ("Tubos de Transporte", "tubos_transporte")
        }),
        2: ("coleta_urina", {
            1: ("Frascos Estéreis", "frascos_estereis"),
            2: ("Frascos de Urina 24h", "frascos_urinas_24h"),
            3: ("Copos Coletores", "copos_coletores")
        }),
        3: ("coleta_fezes", {
            1: ("Máscaras Cirúrgicas", "mascaras_cirurgicas"),
            2: ("Propé", "prope"),
            3: ("Toucas Descartáveis", "toucas_descartaveis"),
            4: ("Sabonete Líquido", "sabonete_liquido"),
            5: ("Papel Toalha", "papel_toalha"),
            6: ("Etiquetas Identificadoras", "etiquetas_identificadoras"),
            7: ("Luvas Descartáveis", "luvas_descartaveis")
        }),
        4: ("materiais_gerais", {
            1: ("Álcool 70%", "alcool_70"),
            2: ("Papel Higiênico", "papel_higienico"),
            3: ("Sacos de Lixo", "sacos_lixo")
        })
    }

    try:
        print("Escolha a categoria do produto:")
        for i, (cat_key, _) in categorias.items():
            nome_formatado = cat_key.replace("_", " ").title()
            print(f"{i}. {nome_formatado}")

        opcao_categoria = int(input("Digite o número da categoria: ").strip())
        categoria_key, produtos = categorias[opcao_categoria]

        print("\nEscolha o produto:")
        for i, (nome_exibicao, _) in produtos.items():
            print(f"{i}. {nome_exibicao}")

        opcao_produto = int(input("Digite o número do produto: ").strip())
        nome_exibicao, item_key = produtos[opcao_produto]

        return categoria_key, item_key

    except (KeyError, ValueError):
        print("Opção inválida. Tente novamente.\n")
        return escolher_produto()

      
from datetime import date

def atualizar_estoque(categoria: str, item: str, quantidade: int, acao: str) -> None:
    """Atualiza o estoque de um item em uma categoria específica e registra consumo diário."""
    estoque = carregar_dados("estoque.json") or {}
    dados_consumo_diario = carregar_dados("consumo_diario.json") or {}
    fila_consumo = dados_consumo_diario["consumo_diario"]
    data_str = date.today().isoformat() #Dia do consumo

    if categoria in estoque.get("insumos", {}):
        if item in estoque["insumos"][categoria]:
            if acao == "adicionar":
                estoque["insumos"][categoria][item] += quantidade
                print(f"{quantidade} unidades adicionadas a '{item}' em '{categoria}'.")

            elif acao == "remover":
                if estoque["insumos"][categoria][item] >= quantidade:
                    estoque["insumos"][categoria][item] -= quantidade
                    print(f"{quantidade} unidades removidas de '{item}' em '{categoria}'.")

                    # Registro de consumo diário
                    if fila_consumo and fila_consumo[-1]["data"] == data_str:
                        if categoria in fila_consumo[-1]:
                            if item in fila_consumo[-1][categoria]:
                                fila_consumo[-1][categoria][item] += quantidade
                            else:
                                fila_consumo[-1][categoria][item] = quantidade
                        else:
                            fila_consumo[-1][categoria] = {item: quantidade}
                    else:
                        fila_consumo.append({
                            "data": data_str,
                            categoria: {item: quantidade}
                        })

                    #FIFO para manter apenas últimos 30 dias
                    consumo_diario_limpar(dados_consumo_diario, limite=30)
                    salvar_dados("consumo_diario.json", dados_consumo_diario)
                    

                else:
                    print(f"Erro: Não há {quantidade} unidades suficientes de '{item}' para remover.")
            else:
                print("Erro: Ação inválida. Use 'adicionar' ou 'remover'.")
        else:
            print(f"Erro: Item '{item}' não encontrado na categoria '{categoria}'.")
    else:
        print(f"Erro: Categoria '{categoria}' não encontrada.")

    # Salvar estoque atualizado sempre
    salvar_dados("estoque.json", estoque)

    input("Pressione Enter para continuar...")


def consumo_diario_limpar(dados_consumo: dict, limite: int = 30) -> None:
    '''Limitar o uso do arquivo consumo_diario.json para os últimos 30 dias.'''
    if "consumo_diario" in dados_consumo:
        fila_consumo = dados_consumo["consumo_diario"]
        while len(fila_consumo) > limite: #FIFO
            fila_consumo.pop(0) # Remove o registro mais antigo


def buscar_produto_estoque():
    '''Busca um produto no estoque usando busca binária.
    Complexidade: O(n log n)'''
    estoque = carregar_dados('estoque.json')
    todos_produtos = []

    for categoria, itens in estoque.get("insumos", {}).items():  # O(n)
        for item in itens:
            todos_produtos.append((item.lower(), categoria))

    if not todos_produtos:
        print("Estoque vazio.")
        input("Pressione Enter para continuar...")
        return

    todos_produtos.sort(key=lambda x: x[0])  # O(n log n)
    nome = input("Digite o nome do produto que deseja buscar: ").strip().lower()

    nomes_ordenados = [item[0] for item in todos_produtos]  # O(n)
    pos = busca_binaria(nomes_ordenados, nome)  # O(log n)

    if pos != -1:
        nome, categoria = todos_produtos[pos]
        quantidade = estoque["insumos"][categoria][nome]
        print(f"Produto encontrado! Categoria: {categoria}, Quantidade: {quantidade}")
    else:
        print("Produto não encontrado.")
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
    '''Atualiza a situação do estoque e salva em situacao_estoque.json.'''
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


def checar_consumo_diario() -> None:
    '''Checa o consumo diário de insumos e exibe ele na tela.'''
    input("Pressione Enter para continuar...")


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