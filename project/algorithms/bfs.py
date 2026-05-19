"""
Módulo de Busca em Largura (Breadth-First Search - BFS).
"""
import time
from collections import deque

def bfs(graph, start_node, target_node):
    """
    Implementação completa do algoritmo BFS (Breadth-First Search).
    
    Contexto Acadêmico:
    O BFS explora de forma uniforme (em anéis de profundidade),
    garantindo encontrar o caminho mais curto (menos saltos).
    Porém, em Knowledge Graphs muito densos e em ambientes de
    Reinforcement Learning, isso pode causar o estouro do limite de memória
    devido à necessidade de manter a fronteira completa na fila.
    
    Complexidade:
    - Tempo: O(V + E)
      Onde V é a quantidade de vértices e E é a quantidade de arestas.
      No pior caso, todas as arestas e nós são visitados.
    - Espaço: O(V)
      Devido à estrutura de controle de visitados e a fila (que pode
      armazenar uma grande quantidade de nós na camada atual).
    
    Args:
        graph (Graph): Instância do grafo a ser explorado.
        start_node (int): Nó de origem inicial.
        target_node (int): Nó de destino desejado.
        
    Returns:
        tuple: (caminho_encontrado, tempo_execucao, nos_visitados)
    """
    start_time = time.perf_counter()
    
    visited = set()
    visited_count = 0
    
    # A fila armazena tuplas com (nó atual, caminho até este nó)
    queue = deque([(start_node, [start_node])])
    visited.add(start_node)
    visited_count += 1
    
    path_found = None
    
    while queue:
        current_node, path = queue.popleft()
        
        # Se encontrou o alvo, encerra a busca imediatamente
        if current_node == target_node:
            path_found = path
            break
            
        # Explora os vizinhos
        for neighbor in graph.get_neighbors(current_node):
            if neighbor not in visited:
                visited.add(neighbor)
                visited_count += 1
                queue.append((neighbor, path + [neighbor]))
                
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    return path_found, execution_time, visited_count
