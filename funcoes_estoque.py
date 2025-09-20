from datetime import datetime
import time
from funcoes_gerais import *
from funcoes_consumo import consumo_diario_limpar, ordenar_fila_consumo_por_data

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
            1: ("Mascaras cirurgícas", "mascaras_cirurgicas"),
            2: ("Prope", "prope"),
            3: ("Papel toalha", "papel_toalha"),
            4: ("Etiquetas identificadoras", "etiquetas_identificadoras"),
            5: ("Luvas descartáveis", "luvas_descartaveis"),
            6: ("Sabonete líquido", "sabonete_liquido"),
            7: ("Toucas descartáveis", "toucas_descartaveis")
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


def registro_aleatorio_estoque() -> dict:
    '''Gera um registro no estoque, registros e no consumo diário com valores aleatórios.'''
    #estoque = carregar_dados('estoque.json')
    #consumo_diario = carregar_dados('consumo_diario.json')
    registros = carregar_dados('registros.json')
    id_registro = gerar_id(registros)
    data_dt = fake.date_time_between(
    start_date='-7d',
    end_date='now') #Gera uma data aleatória entre 7 dias atrás e agora
    data_registro = data_dt.strftime("%d/%m/%Y %H:%M:%S")   # Formatação do datatime para registro
    data_registro_simples = data_dt.strftime("%d/%m/%Y")    # Formatação do datatime para consumo diário
    categoria, produto = escolher_produto_aleatorio()
    tipo_registro = random_choice_registro(produto)
    qtd = random.randint(100, 500)
    registros[id_registro] = {
        'insumo': produto,
        'quantidade': qtd,
        'data_registro': data_registro,
        'tipo_registro': tipo_registro
    }
    #atualizar_estoque(categoria, produto, qtd, tipo_registro, data_registro)
    salvar_dados('registros.json', registros)
    atualizar_estoque(categoria, produto, qtd, tipo_registro, data_registro_simples, aleatorio=True)
    

def registro_periodico() -> None:
    while True:
        try:
            registro_aleatorio_estoque()
        except Exception as e:
            print("Erro na thread:", e)
        time.sleep(5)


def atualizar_estoque(categoria: str, item: str, quantidade: int, acao: str,
                      data: str, aleatorio: bool) -> None:
    estoque = carregar_dados("estoque.json")
    dados_consumo_diario = carregar_dados("consumo_diario.json")
    fila_consumo = dados_consumo_diario["consumo_diario"]

    def log(msg: str) -> None:
        if not aleatorio:
            print(msg)

    if categoria in estoque.get("insumos", {}):
        if item in estoque["insumos"][categoria]:
            if acao == "adicionar":
                estoque["insumos"][categoria][item] += quantidade
                log(f"{quantidade} unidades adicionadas a '{item}' em '{categoria}'.")

            elif acao == "remover":
                if estoque["insumos"][categoria][item] >= quantidade:
                    estoque["insumos"][categoria][item] -= quantidade
                    log(f"{quantidade} unidades removidas de '{item}' em '{categoria}'.")

                    # Registro de consumo diário - usando fila FIFO
                    registro_encontrado = None
                    indice_registro = -1
                    
                    # Procura se já existe registro para esta data (mantém a ordem FIFO)
                    for i, registro in enumerate(fila_consumo):
                        if registro["data"] == data:
                            registro_encontrado = registro
                            indice_registro = i
                            break
                    
                    # Se encontrou registro para a data, atualiza
                    if registro_encontrado:
                        if categoria not in registro_encontrado:
                            registro_encontrado[categoria] = {}
                        if item not in registro_encontrado[categoria]:
                            registro_encontrado[categoria][item] = 0
                        registro_encontrado[categoria][item] += quantidade
                    else:
                        # Adiciona novo registro no final da fila (mantém FIFO)
                        fila_consumo.append({
                            "data": data,
                            categoria: {item: quantidade}
                        })

                    # Consolida registros duplicados da mesma data (mantendo FIFO)
                    # Cria uma nova lista consolidada mantendo a ordem
                    nova_fila = []
                    datas_processadas = []
                    
                    for registro in fila_consumo:
                        data_registro = registro["data"]
                        
                        if data_registro not in datas_processadas:
                            # Primeira vez que vemos esta data - cria registro consolidado
                            registro_consolidado = {"data": data_registro}
                            
                            # Encontra todos os registros com esta data e consolida
                            for outro_registro in fila_consumo:
                                if outro_registro["data"] == data_registro:
                                    for cat, itens in outro_registro.items():
                                        if cat != "data":
                                            if cat not in registro_consolidado:
                                                registro_consolidado[cat] = {}
                                            for item_nome, qtd in itens.items():
                                                if item_nome not in registro_consolidado[cat]:
                                                    registro_consolidado[cat][item_nome] = 0
                                                registro_consolidado[cat][item_nome] += qtd
                            
                            nova_fila.append(registro_consolidado)
                            datas_processadas.append(data_registro)
                    
                    # Substitui a fila original pela fila consolidada
                    dados_consumo_diario["consumo_diario"] = nova_fila
                    fila_consumo = nova_fila
                    
                    # Ordena a fila por data (mais antigo primeiro)
                    ordenar_fila_consumo_por_data(fila_consumo)
                    
                    # Limpa registros antigos (mantém apenas os últimos 7 dias)
                    consumo_diario_limpar(fila_consumo, limite=7)
                    
                    salvar_dados("consumo_diario.json", dados_consumo_diario)
                else:
                    log(f"Erro: Não há {quantidade} unidades suficientes de '{item}' para remover.")
            else:
                log("Erro: Ação inválida. Use 'adicionar' ou 'remover'.")
        else:
            log(f"Erro: Item '{item}' não encontrado na categoria '{categoria}'.")
    else:
        log(f"Erro: Categoria '{categoria}' não encontrada.")

    # Salvar estoque atualizado sempre
    salvar_dados("estoque.json", estoque)
    
    if not aleatorio:
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
                print(f'''ALERTA: O item {item.upper()}
na categoria {categoria.upper()}
está com baixo estoque ({quantidade} unidades).''')
                time.sleep(1)  # Pausa para evitar muitas mensagens de uma vez


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