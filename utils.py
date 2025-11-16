def exibir_estatisticas(blocos):
    # calcula e exibe as estatísticas de armazenamento
    if not blocos:
        print("Nenhum bloco foi gerado.")
        return

    num_blocos = len(blocos)
    tamanho_bloco = blocos[0].tamanho_maximo
    
    total_bytes_ocupados = sum(b.ocupacao for b in blocos)
    total_bytes_disponiveis = num_blocos * tamanho_bloco
    
    percentual_medio = sum(b.percentual_ocupacao for b in blocos) / num_blocos
    num_parcialmente_usados = sum(1 for b in blocos if b.ocupacao > 0 and b.ocupacao < b.tamanho_maximo)
    eficiencia = (total_bytes_ocupados / total_bytes_disponiveis) * 100 if total_bytes_disponiveis > 0 else 0

    print("\n--- ESTATÍSTICAS DE ARMAZENAMENTO ---")
    print(f"Número total de blocos utilizados: {num_blocos}")
    print(f"Percentual de ocupação dos blocos: {percentual_medio:.2f}%")
    print(f"Número de blocos parcialmente utilizados: {num_parcialmente_usados}")
    print(f"Eficiência de armazenamento (bytes úteis / total): {eficiencia:.2f}%")
    
    print("\n--- MAPA DE OCUPAÇÃO DOS BLOCOS ---")
    for bloco in blocos:
        print(f"Bloco {bloco.id}: {bloco.ocupacao} / {bloco.tamanho_maximo} bytes ({bloco.percentual_ocupacao:.2f}% cheio)")
