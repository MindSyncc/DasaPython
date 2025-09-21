from datetime import datetime
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
    #A função 'max' vai comparar os itens da lista e retornar o maior
    ultimo_consumo = max(
        consumos,  # Lista de dicionários, cada um representando um consumo
        key=lambda x: datetime.strptime(
            x["data_registro"],  #Acessa a string da data dentro do dicionário
            "%d/%m/%Y %H:%M:%S"
        )
    )
    insumo_consumido = ultimo_consumo["insumo"]

    #Cria a lista [(insumo, quantidade, prioridade)]
    lista_insumos = []
    for categoria, itens in estoque["insumos"].items():
        for nome, qtd in itens.items():
            prioridade = 0 if nome == insumo_consumido else 1
            lista_insumos.append((nome, qtd, prioridade))

    #Ordena a lista por merge_sort
        lista_ordenada = merge_sort(lista_insumos, key=lambda x: (x[2], x[0]))
    #Reconstrui dicionário ordenado
    insumos_ordenados = {nome: qtd for nome, qtd, _ in lista_ordenada}

    return insumos_ordenados


def checar_consumo_7_dias() -> None:
    """
    Checa o registro dos últimos 7 dias de insumos e exibe do mais antigo
    para o mais recente, usando uma pilha.
    """
    dados_consumo = carregar_dados('consumo_diario.json')

    # Verifica se há registros
    registros = dados_consumo.get("consumo_diario", [])
    if not registros:
        print("Nenhum consumo registrado")
        input("Pressione Enter para continuar...")
        return

    # Ordena os registros por data (mais antigo primeiro)
    registros_ordenados = sorted(registros, 
                               key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y"))
    
    # Pega os últimos 7 registros e empilha (o mais recente fica no topo)
    pilha = []
    for registro in registros_ordenados[-7:]:  # Pega os 7 mais recentes
        pilha.append(registro)
    
    print("Consumo dos últimos 7 dias (mais recente primeiro - usando pilha):")
    print("=" * 60)
    
    if not pilha:
        print("Nenhum consumo registrado nos últimos 7 dias")
    else:
        # Desempilha (LIFO - Last In First Out)
        while pilha:
            registro = pilha.pop()  # Remove do topo (mais recente)
            data = registro.get("data", "Data não disponível")
            print(f"\nData: {data}")
            print("-" * 30)
            
            # Mostra os consumos
            tem_consumo = False
            for chave, valor in registro.items():
                if chave != "data":
                    tem_consumo = True
                    if isinstance(valor, dict):
                        print(f"  {chave}:")
                        for item, quantidade in valor.items():
                            print(f"    - {item}: {quantidade}")
                    else:
                        print(f"  {chave}: {valor}")
            
            if not tem_consumo:
                print("  Nenhum consumo registrado neste dia")

    input("\nPressione Enter para continuar...")

        
def consumo_diario_limpar(dados_consumo: dict, limite: int = 7) -> None:
    '''Limitar o uso do arquivo consumo_diario.json para os últimos 7 dias.'''
    if "consumo_diario" in dados_consumo:
        fila_consumo = dados_consumo["consumo_diario"]
        while len(fila_consumo) > limite: #FIFO
            fila_consumo.pop(0) # Remove o registro mais antigo


def ordenar_fila_consumo_por_data(fila_consumo: list) -> None:
    """Ordena a fila de consumo por data (mais antigo primeiro - mantendo FIFO)"""
    # Ordena por data (mais antigo primeiro para manter a lógica FIFO)
    fila_consumo.sort(key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y"))

def converter_data_para_objeto(data_str: str) -> datetime:
    """Converte string de data no formato DD/MM/AAAA para objeto datetime"""
    return datetime.strptime(data_str, "%d/%m/%Y")
