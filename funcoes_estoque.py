from datetime import datetime, date
from funcoes_gerais import *
from funcoes_consumo import consumo_diario_limpar


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

      
def atualizar_estoque(categoria: str, item: str, quantidade: int, acao: str, data: None) -> None:
    """Atualiza o estoque de um item em uma categoria específica e registra consumo diário."""
    estoque = carregar_dados("estoque.json") or {}
    dados_consumo_diario = carregar_dados("consumo_diario.json") or {}
    fila_consumo = dados_consumo_diario["consumo_diario"]

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
                    if fila_consumo and fila_consumo[-1]["data"] == data:
                        if categoria in fila_consumo[-1]:
                            if item in fila_consumo[-1][categoria]:
                                fila_consumo[-1][categoria][item] += quantidade
                            else:
                                fila_consumo[-1][categoria][item] = quantidade
                        else:
                            fila_consumo[-1][categoria] = {item: quantidade}
                    else:
                        fila_consumo.append({
                            "data": data,
                            categoria: {item: quantidade}
                        })

                    #FIFO para manter apenas últimos 7 dias
                    consumo_diario_limpar(dados_consumo_diario, limite=7)
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