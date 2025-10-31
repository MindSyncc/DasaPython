from funcoes_dinamicas_lucro import *


def testar_programacao_dinamica():
    """Testa todas as versões da Programação Dinâmica"""
    print("=== TESTE DE PROGRAMAÇÃO DINÂMICA ===\n")
    demandas = [120, 180, 160, 200, 170, 190, 150]

    print("Demanda de exemplo(7 dias):", demandas)
    print("\n" + "=" * 50)

    #versão recursiva
    print("1. VERSÃO RECURSIVA (Top-Down):")
    custo_rec, pedido_rec = dp_recursiva_estoque(0, 0, demandas)
    print(f"   Custo mínimo: R${custo_rec:.2f}")
    print(f"   Primeiro pedido recomendado: {pedido_rec} unidades")

    #versão com memorização
    print("\n2. VERSÃO MEMORIZAÇÃO (Otimizada):")
    custo_mem, pedido_mem = dp_memorizacao_estoque(0, 0, demandas)
    print(f"   Custo mínimo: R${custo_mem:.2f}")
    print(f"   Primeiro pedido recomendado: {pedido_mem} unidades")

    #versão iterativa
    print("\n3. VERSÃO ITERATIVA (Bottom-Up):")
    custo_it, pedidos_it = dp_iterativa_estoque(demandas)
    print(f"   Custo mínimo: R${custo_it:.2f}")
    print(f"   Sequência de pedidos: {pedidos_it}")

    print("\n" + "=" * 50)
    print("4. VERIFICAÇÃO DE CONSISTÊNCIA:")
    consistente = verificar_consistencia_dp(demandas)

    if consistente:
        print("TODAS AS VERSões PRODUZEM OS MESMOS RESULTADOS!")
    else:
        print("Há divergências entre as versões")


if __name__ == "__main__":
    testar_programacao_dinamica()