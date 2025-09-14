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


def checar_consumo_diario() -> None:
    '''Checa o consumo diário de insumos e exibe ele na tela.'''
    input("Funcionalidade em desenvolvimento...")
