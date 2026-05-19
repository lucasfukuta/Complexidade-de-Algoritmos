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
    sizes = [100, 1000, 5000, 10000]
    edges_per_node = 4 # Define uma certa densidade/ramificação de Knowledge Graph
    
    print("-" * 75)
    print(f"{'Nodes':<8} | {'Algorithm':<12} | {'Time (s)':<15} | {'Visited':<10} | {'Memory (KiB)':<15}")
    print("-" * 75)
    
    for size in sizes:
        # Gera o grafo dinâmico para a iteração
        graph = generate_graph(size, edges_per_node)
        
        # Iniciar no nó de índice 0
        start_node = f"Entidade_0"
        
        # Define um alvo distante (ou o último) para forçar o pior caso
        target_node = f"Entidade_{size - 1}" 
        
        # Configuração de pipelines experimentais
        tests = [
            ("BFS", lambda: bfs(graph, start_node, target_node)),
            ("DLS k=2", lambda: dls(graph, start_node, target_node, 2)),
            ("DLS k=4", lambda: dls(graph, start_node, target_node, 4)),
            ("DLS k=6", lambda: dls(graph, start_node, target_node, 6))
        ]
        
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
