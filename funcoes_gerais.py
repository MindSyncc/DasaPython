import os
import json
import random
import time
import random
from faker import Faker


fake = Faker("pt_BR")

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


def busca_binaria(lista, alvo):
    '''Realiza uma busca binária em uma lista ordenada. 
    Retorna o índice do alvo ou -1 se não encontrado.'''
    esquerda, direita = 0, len(lista) - 1
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        if lista[meio] == alvo:
            return meio
        elif lista[meio] < alvo:
            esquerda = meio + 1
        else:
            direita = meio - 1
    return -1


def busca_sequencial(lista, alvo):
    '''Realiza uma busca sequencial em uma lista. 
    Retorna o índice do alvo ou -1 se não encontrado.'''
    for i in range(len(lista)):
        if lista[i] == alvo:
            return i
    return -1


def merge_sort(lista):
    '''Ordena uma lista usando o algoritmo merge sort.'''
    if len(lista) <= 1:
        return lista
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio])
    direita = merge_sort(lista[meio:])
    resultado = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        if esquerda[i] < direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1
    while j < len(direita):
        resultado.append(direita[j])
        j += 1
    return resultado


def escolher_produto_aleatorio()-> tuple:
    '''Escolhe um produto aleatório do estoque.'''
    estoque = carregar_dados('estoque.json')
    categorias = list(estoque.get("insumos", {}).keys())
    if not categorias:
        print("Estoque vazio.")
        return None, None
    categoria = random.choice(categorias)
    produtos = list(estoque["insumos"][categoria].keys())
    if not produtos:
        print(f"Nenhum produto na categoria {categoria}.")
        return None, None
    produto = random.choice(produtos)
    return categoria, produto


def random_choice_registro(produto: str) -> str:
    '''Escolhe aleatoriamente entre "adicionar" e "remover" para o registro de estoque.'''
    estoque = carregar_dados('estoque.json')
    for categoria, itens in estoque.get("insumos", {}).items():
        if produto in itens:
            if itens[produto] < 500:
                return "adicionar"
            else:
                return random.choice(["adicionar", "remover"])


def consumo_diario_limpar(dados_consumo: dict, limite: int = 7) -> None:
    '''Limitar o uso do arquivo consumo_diario.json para os últimos 7 dias.'''
    if "consumo_diario" in dados_consumo:
        fila_consumo = dados_consumo["consumo_diario"]
        while len(fila_consumo) > limite: #FIFO
            fila_consumo.pop(0) # Remove o registro mais antigo


def registro_aleatorio_estoque() -> dict:
    '''Gera um registro no estoque, registros e no consumo diário com valores aleatórios.'''
    #estoque = carregar_dados('estoque.json')
    #consumo_diario = carregar_dados('consumo_diario.json')
    registros = carregar_dados('registros.json')
    id_registro = gerar_id(registros)
    data_registro = fake.date_time_this_year().strftime("%d/%m/%Y %H:%M:%S")
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


def worker():
    '''Função worker para adicionar registros aleatórios periodicamente.'''
    while True:
        registro_aleatorio_estoque()
        time.sleep(5)  # Aguarda 5 segundos antes de adicionar o próximo registro

