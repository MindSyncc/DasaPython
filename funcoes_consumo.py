from datetime import datetime
from funcoes_gerais import *
from faker import Faker


fake = Faker("pt_BR")

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
        lista_ordenada = merge_sort(lista_insumos, key=lambda x: (x[2], x[0]))
    #Reconstrui dicionário ordenado
    insumos_ordenados = {nome: qtd for nome, qtd, _ in lista_ordenada}

    return insumos_ordenados


def consumo_diario_limpar(dados_consumo: dict, limite: int = 7) -> None:
    '''Limitar o uso do arquivo consumo_diario.json para os últimos 7 dias.'''
    if "consumo_diario" in dados_consumo:
        fila_consumo = dados_consumo["consumo_diario"]
        while len(fila_consumo) > limite: #FIFO
            fila_consumo.pop(0) # Remove o registro mais antigo


def checar_consumo_diario() -> None:
    '''Checa o consumo diário de insumos e exibe ele na tela.'''
    input("Funcionalidade em desenvolvimento...")


def registro_aleatorio_estoque() -> dict:
    '''Gera um registro no estoque, registros e no consumo diário com valores aleatórios.'''
    #estoque = carregar_dados('estoque.json')
    #consumo_diario = carregar_dados('consumo_diario.json')
    registros = carregar_dados('registros.json')
    id_registro = gerar_id(registros)
    data_registro = fake.date_time_this_year().strftime("%d/%m/%Y %H:%M:%S")
    produto = escolher_produto_aleatorio()
    tipo_registro = random_choice_registro(produto)

    registros[id_registro] = {
        'insumo': produto,
        'quantidade': random.randint(100, 500),
        'data_registro': data_registro,
        'tipo_registro': tipo_registro
    }
    
    salvar_dados('registros.json', registros)


def worker():
    '''Função worker para adicionar registros aleatórios periodicamente.'''
    while True:
        registro_aleatorio_estoque()
        time.sleep(5)  # Aguarda 5 segundos antes de adicionar o próximo registro
