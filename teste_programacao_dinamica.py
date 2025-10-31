from funcoes_dinamicas_lucro import *


def testar_programacao_dinamica():
    """Testa todas as versões da Programação Dinâmica"""
    print("=== TESTE DE PROGRAMAÇÃO DINÂMICA ===\n")

    # Dados de exemplo baseados no consumo real
    demanda_exemplo = [120, 180, 160, 200, 170, 190, 150]

    print("Demanda de exemplo (7 dias):", demanda_exemplo)
    print("\n" + "=" * 50)

    # Testar versão recursiva
    print("1. VERSÃO RECURSIVA (Top-Down):")
    custo_rec, pedido_rec = dp_recursiva_estoque(0, 0, demanda_exemplo)
    print(f"   Custo mínimo: R${custo_rec:.2f}")
    print(f"   Primeiro pedido recomendado: {pedido_rec} unidades")

    # Testar versão com memorização
    print("\n2. VERSÃO MEMORIZAÇÃO (Otimizada):")
    custo_mem, pedido_mem = dp_memorizacao_estoque(0, 0, demanda_exemplo)
    print(f"   Custo mínimo: R${custo_mem:.2f}")
    print(f"   Primeiro pedido recomendado: {pedido_mem} unidades")

    # Testar versão iterativa
    print("\n3. VERSÃO ITERATIVA (Bottom-Up):")
    custo_it, pedidos_it = dp_iterativa_estoque(demanda_exemplo)
    print(f"   Custo mínimo: R${custo_it:.2f}")
    print(f"   Sequência de pedidos: {pedidos_it}")

    # Verificar consistência
    print("\n" + "=" * 50)
    print("4. VERIFICAÇÃO DE CONSISTÊNCIA:")
    consistente = verificar_consistencia_dp(demanda_exemplo)

    if consistente:
        print("✅ TODAS AS VERSões PRODUZEM OS MESMOS RESULTADOS!")
    else:
        print("❌ Há divergências entre as versões")


if __name__ == "__main__":
    testar_programacao_dinamica()