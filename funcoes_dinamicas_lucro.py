from funcoes_gerais import carregar_dados, salvar_dados, limpar_tela
# Cache global para memorização
MEMO_DP = {}


def limpar_memo():
    """Limpa o cache de memorização"""
    global MEMO_DP
    MEMO_DP = {}


def prever_demanda_insumos(dias=7):
    """Preve demanda baseada no consumo histórico - ESTADO"""
    consumo_diario = carregar_dados('consumo_diario.json')
    registros = consumo_diario.get("consumo_diario", [])

    previsoes = {}

    for registro in registros:
        for categoria, itens in registro.items():
            if categoria == "data":
                continue

            if categoria not in previsoes:
                previsoes[categoria] = {}

            for item, quantidade in itens.items():
                if item not in previsoes[categoria]:
                    previsoes[categoria][item] = []
                previsoes[categoria][item].append(quantidade)

    # Calcular média para previsão
    previsao_final = {}
    for categoria, itens in previsoes.items():
        previsao_final[categoria] = {}
        for item, consumos in itens.items():
            if consumos:
                media = sum(consumos) / len(consumos)
                previsao_final[categoria][item] = [int(media)] * dias
            else:
                previsao_final[categoria][item] = [50] * dias  # Valor padrão

    return previsao_final


def dp_recursiva_estoque(dia, estoque_atual, demanda,
                         custo_pedido=120.0, custo_estoque=0.10,
                         custo_falta=5.0, capacidade_max=1000):
    """
    VERSÃO RECURSIVA - Programação Dinâmica Top-Down
    Estados: (dia, estoque_atual)
    Decisões: quantidade a pedir
    Função de transição: novo_estoque = estoque_atual - demanda[dia] + pedido
    Função objetivo: minimizar custo total
    """
    # Caso base: fim do período
    if dia >= len(demanda):
        return 0, 0

    demanda_dia = demanda[dia]

    # Calcular custos do dia atual
    if estoque_atual >= demanda_dia:
        custo_est_dia = (estoque_atual - demanda_dia) * custo_estoque
        custo_falta_dia = 0
        estoque_pos_consumo = estoque_atual - demanda_dia
    else:
        custo_est_dia = 0
        custo_falta_dia = (demanda_dia - estoque_atual) * custo_falta
        estoque_pos_consumo = 0

    # DECISÕES: Explorar diferentes quantidades de pedido
    melhor_custo = float('inf')
    melhor_pedido = 0

    for pedido in range(0, capacidade_max - estoque_pos_consumo + 1, 100):  # Passo de 100 unidades
        custo_pedido_dia = custo_pedido if pedido > 0 else 0

        novo_estoque = min(capacidade_max, estoque_pos_consumo + pedido)

        # FUNÇÃO DE TRANSIÇÃO: chamada recursiva para próximo estado
        custo_futuro, _ = dp_recursiva_estoque(
            dia + 1, novo_estoque, demanda, custo_pedido, custo_estoque, custo_falta, capacidade_max
        )

        # FUNÇÃO OBJETIVO: minimizar custo total
        custo_total = custo_pedido_dia + custo_est_dia + custo_falta_dia + custo_futuro

        if custo_total < melhor_custo:
            melhor_custo = custo_total
            melhor_pedido = pedido

    return melhor_custo, melhor_pedido


def dp_memorizacao_estoque(dia, estoque_atual, demanda,
                           custo_pedido=50.0, custo_estoque=0.10,
                           custo_falta=5.0, capacidade_max=1000):
    """
    VERSÃO MEMORIZAÇÃO - Programação Dinâmica com Cache
    Mesmos estados, decisões e funções da versão recursiva, mas com otimização
    """
    global MEMO_DP

    chave = (dia, estoque_atual)
    if chave in MEMO_DP:
        return MEMO_DP[chave]

    # Caso base
    if dia >= len(demanda):
        return 0, 0

    demanda_dia = demanda[dia]

    # Calcular custos do dia atual
    if estoque_atual >= demanda_dia:
        custo_est_dia = (estoque_atual - demanda_dia) * custo_estoque
        custo_falta_dia = 0
        estoque_pos_consumo = estoque_atual - demanda_dia
    else:
        custo_est_dia = 0
        custo_falta_dia = (demanda_dia - estoque_atual) * custo_falta
        estoque_pos_consumo = 0

    melhor_custo = float('inf')
    melhor_pedido = 0

    for pedido in range(0, capacidade_max - estoque_pos_consumo + 1, 100):
        custo_pedido_dia = custo_pedido if pedido > 0 else 0

        novo_estoque = min(capacidade_max, estoque_pos_consumo + pedido)

        custo_futuro, _ = dp_memorizacao_estoque(
            dia + 1, novo_estoque, demanda, custo_pedido, custo_estoque, custo_falta, capacidade_max
        )

        custo_total = custo_pedido_dia + custo_est_dia + custo_falta_dia + custo_futuro

        if custo_total < melhor_custo:
            melhor_custo = custo_total
            melhor_pedido = pedido

    MEMO_DP[chave] = (melhor_custo, melhor_pedido)
    return melhor_custo, melhor_pedido


def dp_iterativa_estoque(demanda, estoque_inicial=0,
                         custo_pedido=50.0, custo_estoque=0.10,
                         custo_falta=5.0, capacidade_max=1000):
    """
    VERSÃO ITERATIVA - Programação Dinâmica Bottom-Up
    Preenche tabela DP iterativamente
    """
    n_dias = len(demanda)

    # Inicializar tabelas DP
    dp = [[float('inf')] * (capacidade_max + 1) for _ in range(n_dias + 1)]
    pedidos = [[0] * (capacidade_max + 1) for _ in range(n_dias + 1)]

    # Caso base: último dia
    for estoque in range(capacidade_max + 1):
        dp[n_dias][estoque] = 0

    # Preencher tabela de trás para frente
    for dia in range(n_dias - 1, -1, -1):
        for estoque in range(capacidade_max + 1):
            demanda_dia = demanda[dia]

            # Calcular custos do dia atual
            if estoque >= demanda_dia:
                custo_est_dia = (estoque - demanda_dia) * custo_estoque
                custo_falta_dia = 0
                estoque_pos_consumo = estoque - demanda_dia
            else:
                custo_est_dia = 0
                custo_falta_dia = (demanda_dia - estoque) * custo_falta
                estoque_pos_consumo = 0

            melhor_custo = float('inf')
            melhor_pedido = 0

            for pedido in range(0, capacidade_max - estoque_pos_consumo + 1, 100):
                custo_pedido_dia = custo_pedido if pedido > 0 else 0

                novo_estoque = min(capacidade_max, estoque_pos_consumo + pedido)
                custo_futuro = dp[dia + 1][novo_estoque]

                custo_total = custo_pedido_dia + custo_est_dia + custo_falta_dia + custo_futuro

                if custo_total < melhor_custo:
                    melhor_custo = custo_total
                    melhor_pedido = pedido

            dp[dia][estoque] = melhor_custo
            pedidos[dia][estoque] = melhor_pedido

    # Reconstruir sequência ótima de pedidos
    sequencia_pedidos = []
    estoque_atual = estoque_inicial

    for dia in range(n_dias):
        pedido_otimo = pedidos[dia][estoque_atual]
        sequencia_pedidos.append(pedido_otimo)

        # Atualizar estoque para próximo dia
        demanda_dia = demanda[dia]
        if estoque_atual >= demanda_dia:
            estoque_atual = min(capacidade_max, estoque_atual - demanda_dia + pedido_otimo)
        else:
            estoque_atual = min(capacidade_max, pedido_otimo)

    return dp[0][estoque_inicial], sequencia_pedidos


def verificar_consistencia_dp(demanda):
    """Verifica se as três versões produzem os mesmos resultados"""
    limpar_memo()

    # Calcular com cada versão
    custo_rec, pedido_rec = dp_recursiva_estoque(0, 0, demanda)
    custo_mem, pedido_mem = dp_memorizacao_estoque(0, 0, demanda)
    custo_it, pedidos_it = dp_iterativa_estoque(demanda)

    # Verificar consistência dos custos
    custos_consistentes = (abs(custo_rec - custo_mem) < 0.01 and
                           abs(custo_rec - custo_it) < 0.01)

    print(f"=== VERIFICAÇÃO DE CONSISTÊNCIA ===")
    print(f"Recursiva:  R${custo_rec:.2f}, Primeiro pedido: {pedido_rec}")
    print(f"Memorização: R${custo_mem:.2f}, Primeiro pedido: {pedido_mem}")
    print(f"Iterativa:  R${custo_it:.2f}, Sequência: {pedidos_it}")
    print(f"Resultados consistentes: {custos_consistentes}")
    print("=" * 50)

    return custos_consistentes


def otimizar_reposicao_insumos():
    """Função principal que otimiza a reposição de todos os insumos"""
    previsoes = prever_demanda_insumos(7)  # Prever 7 dias
    estoque_atual = carregar_dados('estoque.json')
    resultados = {}

    print("=== OTIMIZAÇÃO DE REPOSIÇÃO - PROGRAMÇÃO DINÂMICA ===")

    for categoria, itens in previsoes.items():
        resultados[categoria] = {}

        for item, demanda in itens.items():
            print(f"\n--- {categoria} - {item} ---")
            print(f"Demanda prevista: {demanda}")

            # Obter estoque atual do item
            estoque_inicial = estoque_atual.get("insumos", {}).get(categoria, {}).get(item, 0)
            print(f"Estoque atual: {estoque_inicial}")

            # Calcular otimização com versão iterativa (mais eficiente)
            custo_otimo, pedidos_otimos = dp_iterativa_estoque(demanda, estoque_inicial)

            resultados[categoria][item] = {
                'demanda_prevista': demanda,
                'estoque_atual': estoque_inicial,
                'custo_minimo': custo_otimo,
                'pedidos_recomendados': pedidos_otimos,
                'reposicao_hoje': pedidos_otimos[0] if pedidos_otimos else 0
            }

            print(f"Custo mínimo: R${custo_otimo:.2f}")
            print(f"Pedidos recomendados: {pedidos_otimos}")
            print(f"Reposição hoje: {pedidos_otimos[0]}")

    # Verificar consistência entre as versões (usando primeiro item como exemplo)
    if previsoes and itens:
        primeiro_item_demanda = list(itens.values())[0]
        verificar_consistencia_dp(primeiro_item_demanda)

    return resultados


def salvar_recomendacoes(recomendacoes):
    """Salva as recomendações de reposição em arquivo JSON"""
    salvar_dados('recomendacoes_reposicao.json', recomendacoes)
    print("\n✅ Recomendações salvas em 'recomendacoes_reposicao.json'")


# Função para integrar com o menu existente
def menu_otimizacao_dp():
    """Menu para otimização com Programação Dinâmica"""
    while True:
        limpar_tela()
        print("=" * 50)
        print("   PROGRAMAÇÃO DINÂMICA - OTIMIZAÇÃO DE ESTOQUE")
        print("=" * 50)
        print("1. Otimizar reposição de todos os insumos")
        print("2. Verificar consistência dos algoritmos")
        print("3. Voltar ao menu principal")
        print("=" * 50)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            recomendacoes = otimizar_reposicao_insumos()
            salvar_recomendacoes(recomendacoes)
            input("\nPressione Enter para continuar...")

        elif opcao == '2':
            # Testar com demanda exemplo
            demanda_teste = [100, 150, 200, 180, 160, 170, 190]
            verificar_consistencia_dp(demanda_teste)
            input("\nPressione Enter para continuar...")

        elif opcao == '3':
            break

        else:
            print("Opção inválida!")
            input("Pressione Enter para continuar...")