from funcoes_gerais import carregar_dados, salvar_dados, limpar_tela
from datetime import datetime, timedelta
import random

# Cache global para memorização
MEMO_DP = {}


def limpar_memo():
    """Limpa o cache de memorização para nova execução"""
    global MEMO_DP
    MEMO_DP = {}


def prever_demanda_insumos(dias=7):
    """Preve a demanda dos insumos baseada no consumo histórico"""
    consumo_diario = carregar_dados('consumo_diario.json')
    registros = consumo_diario.get("consumo_diario", [])[-14:]  # Usamos as últimas 2 semanas

    previsoes = {}

    # Coletamos dados históricos de consumo
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

    # Calculamos a média para previsão futura
    previsao_final = {}
    for categoria, itens in previsoes.items():
        previsao_final[categoria] = {}
        for item, consumos in itens.items():
            if consumos:
                media = sum(consumos) / len(consumos)
                previsao_final[categoria][item] = [int(media)] * dias
            else:
                # Valor padrão quando não há histórico
                previsao_final[categoria][item] = [50] * dias

    return previsao_final


def dp_recursiva_estoque(dia, estoque_atual, demanda,
                         custo_pedido=50.0, custo_estoque=0.10,
                         custo_falta=5.0, capacidade_max=1000):
    """
    Versão recursiva da programação dinâmica - abordagem Top-Down
    Esta função explora todas as possibilidades de forma recursiva
    """
    # Caso base: quando chegamos ao final do período
    if dia >= len(demanda):
        return 0, 0

    demanda_dia = demanda[dia]

    # Calculamos os custos do dia atual
    if estoque_atual >= demanda_dia:
        custo_est_dia = (estoque_atual - demanda_dia) * custo_estoque
        custo_falta_dia = 0
        estoque_pos_consumo = estoque_atual - demanda_dia
    else:
        custo_est_dia = 0
        custo_falta_dia = (demanda_dia - estoque_atual) * custo_falta
        estoque_pos_consumo = 0

    # Exploramos diferentes quantidades de pedido
    melhor_custo = float('inf')
    melhor_pedido = 0

    max_pedido = capacidade_max - estoque_pos_consumo
    for pedido in range(0, max_pedido + 1, 100):  # Consideramos pedidos em lotes de 100
        custo_pedido_dia = custo_pedido if pedido > 0 else 0

        novo_estoque = min(capacidade_max, estoque_pos_consumo + pedido)

        # Chamada recursiva para o próximo dia
        custo_futuro, _ = dp_recursiva_estoque(
            dia + 1, novo_estoque, demanda, custo_pedido, custo_estoque, custo_falta, capacidade_max
        )

        # Calculamos o custo total desta decisão
        custo_total = custo_pedido_dia + custo_est_dia + custo_falta_dia + custo_futuro

        if custo_total < melhor_custo:
            melhor_custo = custo_total
            melhor_pedido = pedido

    return melhor_custo, melhor_pedido


def dp_memorizacao_estoque(dia, estoque_atual, demanda,
                           custo_pedido=50.0, custo_estoque=0.10,
                           custo_falta=5.0, capacidade_max=1000):
    """
    Versão com memorização - otimizamos a recursiva armazenando resultados
    """
    global MEMO_DP

    chave = (dia, estoque_atual)
    if chave in MEMO_DP:
        return MEMO_DP[chave]

    # Caso base
    if dia >= len(demanda):
        return 0, 0

    demanda_dia = demanda[dia]

    # Calculamos os custos do dia atual
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

    max_pedido = capacidade_max - estoque_pos_consumo
    for pedido in range(0, max_pedido + 1, 100):
        custo_pedido_dia = custo_pedido if pedido > 0 else 0

        novo_estoque = min(capacidade_max, estoque_pos_consumo + pedido)

        custo_futuro, _ = dp_memorizacao_estoque(
            dia + 1, novo_estoque, demanda, custo_pedido, custo_estoque, custo_falta, capacidade_max
        )

        custo_total = custo_pedido_dia + custo_est_dia + custo_falta_dia + custo_futuro

        if custo_total < melhor_custo:
            melhor_custo = custo_total
            melhor_pedido = pedido

    # Armazenamos o resultado no cache
    MEMO_DP[chave] = (melhor_custo, melhor_pedido)
    return melhor_custo, melhor_pedido


def dp_iterativa_estoque(demanda, estoque_inicial=0,
                         custo_pedido=50.0, custo_estoque=0.10,
                         custo_falta=5.0, capacidade_max=1000):
    """
    Versão iterativa da programação dinâmica - abordagem Bottom-Up
    Construímos a solução do menor subproblema para o maior
    """
    n_dias = len(demanda)

    # Inicializamos as tabelas de programação dinâmica
    dp = [[float('inf')] * (capacidade_max + 1) for _ in range(n_dias + 1)]
    pedidos = [[0] * (capacidade_max + 1) for _ in range(n_dias + 1)]

    # Caso base: no último dia não há custos futuros
    for estoque in range(capacidade_max + 1):
        dp[n_dias][estoque] = 0

    # Preenchemos a tabela de trás para frente
    for dia in range(n_dias - 1, -1, -1):
        for estoque in range(capacidade_max + 1):
            demanda_dia = demanda[dia]

            # Calculamos os custos para o estado atual
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

            max_pedido = capacidade_max - estoque_pos_consumo
            for pedido in range(0, max_pedido + 1, 100):
                custo_pedido_dia = custo_pedido if pedido > 0 else 0

                novo_estoque = min(capacidade_max, estoque_pos_consumo + pedido)
                custo_futuro = dp[dia + 1][novo_estoque]

                custo_total = custo_pedido_dia + custo_est_dia + custo_falta_dia + custo_futuro

                if custo_total < melhor_custo:
                    melhor_custo = custo_total
                    melhor_pedido = pedido

            dp[dia][estoque] = melhor_custo
            pedidos[dia][estoque] = melhor_pedido

    # Reconstruímos a sequência ótima de pedidos
    sequencia_pedidos = []
    estoque_atual = min(estoque_inicial, capacidade_max)

    for dia in range(n_dias):
        estoque_atual = min(estoque_atual, capacidade_max)
        pedido_otimo = pedidos[dia][estoque_atual]
        sequencia_pedidos.append(pedido_otimo)

        # Atualizamos o estoque para o próximo dia
        demanda_dia = demanda[dia]
        if estoque_atual >= demanda_dia:
            estoque_atual = min(capacidade_max, estoque_atual - demanda_dia + pedido_otimo)
        else:
            estoque_atual = min(capacidade_max, pedido_otimo)

    return dp[0][min(estoque_inicial, capacidade_max)], sequencia_pedidos


def verificar_consistencia_dp(demanda):
    """Verificamos se as três versões produzem os mesmos resultados"""
    limpar_memo()

    # Calculamos com cada versão
    custo_rec, pedido_rec = dp_recursiva_estoque(0, 0, demanda)
    custo_mem, pedido_mem = dp_memorizacao_estoque(0, 0, demanda)
    custo_it, pedidos_it = dp_iterativa_estoque(demanda)

    # Verificamos a consistência dos custos
    custos_consistentes = (abs(custo_rec - custo_mem) < 0.01 and
                           abs(custo_rec - custo_it) < 0.01)

    print("VERIFICACAO DE CONSISTENCIA")
    print("=" * 50)
    print(f"Recursiva:  R${custo_rec:.2f}, Primeiro pedido: {pedido_rec}")
    print(f"Memorizacao: R${custo_mem:.2f}, Primeiro pedido: {pedido_mem}")
    print(f"Iterativa:  R${custo_it:.2f}, Sequencia: {pedidos_it}")
    print(f"Resultados consistentes: {custos_consistentes}")
    print("=" * 50)

    return custos_consistentes


def gerar_datas_recomendacao(dias=7):
    """Geramos as datas para os próximos dias das recomendações"""
    hoje = datetime.now()
    datas = []
    for i in range(dias):
        data = hoje + timedelta(days=i)
        datas.append(data.strftime("%d/%m/%Y"))
    return datas


def otimizar_reposicao_insumos():
    """Função principal que otimiza a reposição de todos os insumos"""
    previsoes = prever_demanda_insumos(7)  # Preve os próximos 7 dias
    estoque_atual = carregar_dados('estoque.json')
    resultados = {
        "data_geracao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "periodo_analisado": "Proximos 7 dias",
        "recomendacoes_por_categoria": {}
    }

    limpar_tela()
    print("OTIMIZACAO DE REPOSICAO - PROGRAMACAO DINAMICA")
    print("=" * 60)
    print(f"Data da analise: {resultados['data_geracao']}")
    print(f"Periodo analisado: {resultados['periodo_analisado']}")
    print("=" * 60)

    # Geramos datas para as recomendações
    datas = gerar_datas_recomendacao(7)

    for categoria, itens in previsoes.items():
        resultados["recomendacoes_por_categoria"][categoria] = {
            "itens": {},
            "resumo_categoria": {
                "total_itens": len(itens),
                "total_reposicao_hoje": 0,
                "custo_total_previsto": 0
            }
        }

        print(f"\nCATEGORIA: {categoria.upper()}")
        print("-" * 50)

        for item, demanda in itens.items():
            print(f"\n   Item: {item}")
            print(f"   Demanda prevista: {demanda}")

            # Obtemos o estoque atual do item
            estoque_inicial = estoque_atual.get("insumos", {}).get(categoria, {}).get(item, 0)
            print(f"   Estoque atual: {estoque_inicial}")

            # Calculamos a otimização com a versão iterativa
            try:
                custo_otimo, pedidos_otimos = dp_iterativa_estoque(demanda, estoque_inicial)

                # Criamos estrutura detalhada por dia
                recomendacoes_detalhadas = []
                for i, (data, pedido, demanda_dia) in enumerate(zip(datas, pedidos_otimos, demanda)):
                    acao = "PEDIDO URGENTE" if pedido > 0 and i == 0 else "PEDIDO" if pedido > 0 else "MANTER"
                    recomendacoes_detalhadas.append({
                        "dia": i + 1,
                        "data": data,
                        "pedido_recomendado": pedido,
                        "demanda_prevista": demanda_dia,
                        "acao": acao
                    })

                # Adicionamos ao resultado
                resultados["recomendacoes_por_categoria"][categoria]["itens"][item] = {
                    'estoque_atual': estoque_inicial,
                    'demanda_prevista_7_dias': demanda,
                    'custo_minimo_previsto': round(custo_otimo, 2),
                    'recomendacoes_diarias': recomendacoes_detalhadas,
                    'resumo_item': {
                        'reposicao_hoje': pedidos_otimos[0],
                        'total_pedidos_7_dias': sum(pedidos_otimos),
                        'status': "URGENTE" if pedidos_otimos[0] > 0 else "NORMAL"
                    }
                }

                # Atualizamos o resumo da categoria
                resultados["recomendacoes_por_categoria"][categoria]["resumo_categoria"]["total_reposicao_hoje"] += \
                pedidos_otimos[0]
                resultados["recomendacoes_por_categoria"][categoria]["resumo_categoria"][
                    "custo_total_previsto"] += custo_otimo

                print(f"   Custo minimo: R${custo_otimo:.2f}")
                print(f"   Recomendacoes:")
                for rec in recomendacoes_detalhadas[:3]:  # Mostramos apenas 3 primeiros dias
                    status = "[URGENTE]" if rec["acao"] == "PEDIDO URGENTE" else "[PEDIDO]" if rec[
                                                                                                   "pedido_recomendado"] > 0 else "[OK]"
                    print(f"      {rec['data']}: {rec['pedido_recomendado']} unidades {status}")
                if len(recomendacoes_detalhadas) > 3:
                    print(f"      ... e mais {len(recomendacoes_detalhadas) - 3} dias")

            except Exception as e:
                print(f"   Erro ao calcular otimizacao: {e}")
                resultados["recomendacoes_por_categoria"][categoria]["itens"][item] = {
                    'erro': str(e),
                    'estoque_atual': estoque_inicial,
                    'demanda_prevista': demanda
                }

    # Adicionamos resumo geral
    resultados["resumo_geral"] = {
        "total_categorias": len(resultados["recomendacoes_por_categoria"]),
        "total_itens_analisados": sum(
            cat["resumo_categoria"]["total_itens"] for cat in resultados["recomendacoes_por_categoria"].values()),
        "reposicao_total_hoje": sum(cat["resumo_categoria"]["total_reposicao_hoje"] for cat in
                                    resultados["recomendacoes_por_categoria"].values()),
        "custo_total_previsto": round(sum(cat["resumo_categoria"]["custo_total_previsto"] for cat in
                                          resultados["recomendacoes_por_categoria"].values()), 2)
    }

    # Verificamos consistência entre as versões
    if previsoes:
        primeira_categoria = list(previsoes.keys())[0]
        if primeira_categoria in previsoes and previsoes[primeira_categoria]:
            primeiro_item = list(previsoes[primeira_categoria].keys())[0]
            primeiro_item_demanda = previsoes[primeira_categoria][primeiro_item]
            print("\n" + "=" * 60)
            verificar_consistencia_dp(primeiro_item_demanda)

    return resultados


def salvar_recomendacoes(recomendacoes):
    """Salvamos as recomendações de reposição em arquivo JSON"""
    salvar_dados('recomendacoes_reposicao.json', recomendacoes)
    print("\nRecomendacoes salvas em 'recomendacoes_reposicao.json'")


def exibir_resumo_recomendacoes(recomendacoes):
    """Exibimos um resumo das recomendações na tela"""
    limpar_tela()
    print("RESUMO DAS RECOMENDACOES DE REPOSICAO")
    print("=" * 50)
    print(f"Data da analise: {recomendacoes['data_geracao']}")
    print(f"Periodo: {recomendacoes['periodo_analisado']}")
    print(f"Total de categorias: {recomendacoes['resumo_geral']['total_categorias']}")
    print(f"Total de itens analisados: {recomendacoes['resumo_geral']['total_itens_analisados']}")
    print(f"Reposicao total para hoje: {recomendacoes['resumo_geral']['reposicao_total_hoje']} unidades")
    print(f"Custo total previsto: R${recomendacoes['resumo_geral']['custo_total_previsto']:.2f}")
    print("\n" + "=" * 50)

    for categoria, dados_categoria in recomendacoes['recomendacoes_por_categoria'].items():
        print(f"\nCATEGORIA: {categoria.upper()}")
        print(f"   Itens: {dados_categoria['resumo_categoria']['total_itens']}")
        print(f"   Reposicao hoje: {dados_categoria['resumo_categoria']['total_reposicao_hoje']} unidades")
        print(f"   Custo previsto: R${dados_categoria['resumo_categoria']['custo_total_previsto']:.2f}")


def menu_otimizacao_dp():
    """Menu para otimização com Programação Dinâmica"""

    while True:
        limpar_tela()
        print("=" * 50)
        print("   PROGRAMACAO DINAMICA - OTIMIZACAO DE ESTOQUE")
        print("=" * 50)
        print("1. Otimizar reposicao de todos os insumos")
        print("2. Verificar consistencia dos algoritmos")
        print("3. Voltar ao menu principal")
        print("=" * 50)

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == '1':
            try:
                recomendacoes = otimizar_reposicao_insumos()
                salvar_recomendacoes(recomendacoes)
                print("\n" + "=" * 50)
                exibir_resumo_recomendacoes(recomendacoes)
            except Exception as e:
                print(f"Erro durante a otimizacao: {e}")
            input("\nPressione Enter para continuar...")

        elif opcao == '2':
            limpar_tela()
            # Testamos com demanda de exemplo
            demanda_teste = []
            for i in range(7):
                demanda_teste.append(random.randint(100,300))
            verificar_consistencia_dp(demanda_teste)
            input("\nPressione Enter para continuar...")

        elif opcao == '3':
            break

        else:
            print("Opcao invalida!")
            input("Pressione Enter para continuar...")