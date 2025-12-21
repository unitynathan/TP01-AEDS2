def calcular_metricas(blocos):
    """
    Analisa os blocos para extrair estatísticas de ocupação e eficiência.
    Essencial para o relatório de reorganização (Antes vs Depois).
    """
    if not blocos:
        return {
            "blocos": 0, 
            "ativos": 0, 
            "excluidos": 0, 
            "eficiencia": 0, 
            "ocupacao_media": 0
        }
    
    total_blocos = len(blocos)
    tamanho_bloco = blocos[0].tamanho_maximo
    total_bytes_arquivo = total_blocos * tamanho_bloco
    
    bytes_ativos = 0
    cont_ativos = 0
    cont_excluidos = 0
    soma_percentuais = 0

    for bloco in blocos:
        soma_percentuais += bloco.percentual_ocupacao
        
        # Percorre cada registro dentro do bloco usando o gerador do TP02
        for offset, status, tam, mat in bloco.percorrer_registros():
            if status == 'A':
                bytes_ativos += tam
                cont_ativos += 1
            else:
                cont_excluidos += 1

    # Eficiência = (Espaço Útil / Espaço Total do Arquivo)
    eficiencia = (bytes_ativos / total_bytes_arquivo) * 100 if total_bytes_arquivo > 0 else 0
    ocupacao_media = soma_percentuais / total_blocos

    return {
        "blocos": total_blocos,
        "ativos": cont_ativos,
        "excluidos": cont_excluidos,
        "eficiencia": eficiencia,
        "ocupacao_media": ocupacao_media
    }

def exibir_comparativo(antes, depois):
    """
    Gera o relatório formatado conforme a Especificação 5 do Manual.
    """
    print("\n" + "="*40)
    print("===== RELATÓRIO DE REORGANIZAÇÃO =====")
    print("="*40)
    
    print("\nAntes:")
    print(f"  Blocos: {antes['blocos']}")
    print(f"  Ocupação média: {antes['ocupacao_media']:.1f}%")
    print(f"  Eficiência total: {antes['eficiencia']:.1f}%")
    
    print("\nDepois:")
    print(f"  Blocos: {depois['blocos']}")
    print(f"  Ocupação média: {depois['ocupacao_media']:.1f}%")
    print(f"  Eficiência total: {depois['eficiencia']:.1f}%")
    
    ganho = depois['eficiencia'] - antes['eficiencia']
    blocos_liberados = antes['blocos'] - depois['blocos']
    
    print("\n" + "-"*40)
    print(f"Ganho de eficiência: {ganho:+.2f}%")
    print(f"Blocos liberados: {blocos_liberados}")
    print("="*40)

def exibir_estatisticas(blocos):
    """
    Exibe o mapa de ocupação física e o resumo de registros (Requisito 5).
    """
    m = calcular_metricas(blocos)
    
    print("\n" + "-"*30)
    print("ESTATÍSTICAS DE ARMAZENAMENTO")
    print("-"*30)
    print(f"Registros Ativos:   {m['ativos']}")
    print(f"Registros Excluídos: {m['excluidos']} (espaço vago)")
    print(f"Eficiência Real:     {m['eficiencia']:.2f}%")
    print(f"Total de Blocos:     {m['blocos']}")
    
    print("\n--- MAPA DE OCUPAÇÃO DOS BLOCOS ---")
    for b in blocos:
        # Mostra quanto do bloco está realmente preenchido por bytes (incluindo excluídos)
        print(f"Bloco {b.id:02d}: {b.ocupacao:4d} / {b.tamanho_maximo} bytes ({b.percentual_ocupacao:6.2f}% cheio)")
    print("-" * 40)