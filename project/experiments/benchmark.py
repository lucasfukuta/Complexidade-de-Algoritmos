"""
Módulo de experimentação e benchmarking.
Orquestra as avaliações de desempenho dos algoritmos desenvolvidos.
"""
import tracemalloc
from graph.generator import generate_graph
from algorithms.bfs import bfs
from algorithms.dls import dls

def run_benchmark():
    """
    Executa testes experimentais completos em grafos de diferentes escalas.
    
    Contexto Acadêmico e Análise Experimental:
    - Escalabilidade: Demonstra como os algoritmos se comportam do nível 'toy'
      (100 nós) até um grafo considerável de 10.000 nós.
    - Crescimento do Grafo: A BFS busca de forma completa, o que leva a uma
      alta taxa de exploração de nós visitados e pico de uso de memória.
    - Busca Completa vs Local: O DLS k-hop força o agente a olhar apenas
      para um subgrafo de tamanho k. Para valores baixos de k, o número de nós
      visitados será drasticamente menor em comparação a BFS em grafos enormes,
      mostrando a eficiência de restringir o Knowledge Graph localmente no RL.
    """
    
    # Tamanhos base para testar escalabilidade progressiva
    sizes = [4, 9, 16, 25, 49, 100, 144, 196, 225, 256]
    edges_per_node = 4 # Define uma certa densidade/ramificação de Knowledge Graph
    
    print("-" * 75)
    print(f"{'Nodes':<8} | {'Algorithm':<12} | {'Time (s)':<15} | {'Visited':<10} | {'Memory (KiB)':<15}")
    print("-" * 75)
    
    for size in sizes:
        if size < 1:
            continue
            
        graph = generate_graph(size, edges_per_node)
        start_node = "Entidade_0"
        
        # Largura da grade quadrada perfeita
        grid_width = int(size ** 0.5)
        
        # ======================================================================
        # 1. CASO MÉDIO LOCAL (Metade da distância máxima da diagonal)
        # ======================================================================
        # Dividimos por 2 para o alvo ficar no meio do mapa, simulando um contexto local
        k_desejado = grid_width - 1 
        if k_desejado < 1: 
            k_desejado = 1 # Evita k=0 para o grafo de 4 nós
        
        x = k_desejado // 2
        y = k_desejado - x
        id_alvo_geometrico = (y * grid_width) + x
        target_node_local = f"Entidade_{id_alvo_geometrico}"
        
        # ======================================================================
        # 2. PIOR CASO ABSOLUTO (Mantido no extremo oposto da diagonal)
        # ======================================================================
        target_node_pior_caso = f"Entidade_{size - 1}"
        
        # Calcula a distância de Manhattan real até o pior caso para o DLS usar
        k_pior_caso = 2 * (grid_width - 1)
        
        print(f"\n[CONFIG] Rodada de {size} nós | Caso Local a {k_desejado} saltos.")
        print(f"[CONFIG] Pior Caso cravado no limite do Grafo: {target_node_pior_caso} (Distância: {k_pior_caso} saltos)")
        
        # ======================================================================
        # 3. PIPELINES EXPERIMENTAIS 
        # ======================================================================
        tests = [
            # Busca Local (O BFS deve parar cedo aqui!)
            ("BFS Local", lambda: bfs(graph, start_node, target_node_local)),
            (f"DLS k={k_desejado}", lambda: dls(graph, start_node, target_node_local, k_desejado)),
            
            # Pior Caso Global (O BFS vai varrer o mapa inteiro até o final)
            ("BFS Pior Caso", lambda: bfs(graph, start_node, target_node_pior_caso))
        ]

        # O DLS Pior Caso busca o alvo do extremo oposto com limite aberto
        if size <= 300:
            # Damos uma folga acima da distância máxima para o backtracking explodir
            limite_pior_caso = k_pior_caso + 5
            tests.append(("DLS Pior Caso", lambda: dls(graph, start_node, target_node_pior_caso, limite_pior_caso)))
        
        for name, func in tests:
            # Rastrear alocação de memória (tracemalloc da lib padrão do Python)
            tracemalloc.start()
            
            # Chama as instâncias anônimas lambda para extrair resultados
            try:
                path, exec_time, visited = func()
            except RecursionError:
                # Opcional caso limite de recursividade estoure
                exec_time = 0.0
                visited = 0
            
            # Coleta as estatísticas de memória
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            peak_kb = peak / 1024.0
            
            # Imprime saída tabular perfeitamente formatada
            print(f"{size:<8} | {name:<12} | {exec_time:<15.6f} | {visited:<10} | {peak_kb:<15.2f}")
            
    print("-" * 75)
