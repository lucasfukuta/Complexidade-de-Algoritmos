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
    sizes = [1, 5, 10, 20, 50, 100, 150, 200, 250]
    edges_per_node = 4 # Define uma certa densidade/ramificação de Knowledge Graph
    
    print("-" * 75)
    print(f"{'Nodes':<8} | {'Algorithm':<12} | {'Time (s)':<15} | {'Visited':<10} | {'Memory (KiB)':<15}")
    print("-" * 75)
    
    for size in sizes:
        # Gera o grafo na escala atual
        graph = generate_graph(size, edges_per_node)
        
        start_node = "Entidade_0"
        
        # Define o 'k' (quantidade de saltos) que você quer testar nesta rodada.
        # Podemos ligar o 'k' ao tamanho do mapa para testar distâncias cada vez maiores.
        grid_width = int(size ** 0.5)
        
        # Define o k dinâmico como a distância máxima aproximada do mapa
        k_desejado = 2 * (grid_width - 1) 
        
        # Calcula as coordenadas (x, y) para dar exatamente 'k' saltos
        x = k_desejado // 2
        y = k_desejado - x
        
        # Converte as coordenadas (x, y) no ID de string que o seu gerador usa
        id_alvo_geometrico = (y * grid_width) + x
        target_node = f"Entidade_{id_alvo_geometrico}"
        
        # PIOR CASO ABSOLUTO: Alvo na ponta extrema oposta da grade
        target_node_pior_caso = f"Entidade_{size - 1}"
        
        print(f"\n[CONFIG] Rodada de {size} nós | Alvo posicionado a {k_desejado} saltos de distância.")
        
        # Configuração de pipelines experimentais usando o MESMO k para todos
        tests = [
            (f"BFS (Alvo k={k_desejado})", lambda: bfs(graph, start_node, target_node)),
            ("BFS Pior Caso", lambda: bfs(graph, start_node, target_node_pior_caso)),
            (f"DLS k={k_desejado}", lambda: dls(graph, start_node, target_node, k_desejado))
        ]

        # O DLS Pior Caso com limite aberto (backtracking exaustivo) só entra em grafos pequenos
        if size <= 1000:
            tests.append(("DLS Pior Caso", lambda: dls(graph, start_node, target_node, k_desejado + 10)))
        
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
