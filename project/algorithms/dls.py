"""
Módulo de Busca Limitada por Profundidade (Depth-Limited Search - DLS).
"""
import time

def dls_recursive(graph, current_node, target_node, limit, path, visited_count_ref):
    """
    Função auxiliar recursiva que implementa a lógica do DLS k-hop.
    Mantém o caminho percorrido para evitar ciclos e realiza backtracking.
    """
    # Adiciona nó ao caminho atual (funciona como controle de visitas locais para ciclos)
    path.append(current_node)
    # Incrementa a referência de contagem total de nós visitados pelo algoritmo
    visited_count_ref[0] += 1
    
    # Checagem de objetivo
    if current_node == target_node:
        return list(path)
        
    # Controle rigoroso de limite k-hop
    if limit <= 0:
        path.pop()
        return None
        
    # Expansão para os nós vizinhos
    for neighbor in graph.get_neighbors(current_node):
        # Evitar loop infinito no caminho atual
        if neighbor not in path:
            result = dls_recursive(graph, neighbor, target_node, limit - 1, path, visited_count_ref)
            if result is not None:
                return result
                
    # Backtracking: remove do caminho após explorar todo o subgrafo deste nó
    path.pop()
    return None

def dls(graph, start_node, target_node, k_hop):
    """
    Implementação do algoritmo DLS (Depth-Limited Search) limitado por k-hop.
    
    Contexto Acadêmico:
    Ao contrário da BFS, o DLS não armazena a grande fronteira de expansão.
    Em KGs usados por agentes em Reinforcement Learning, muitas vezes 
    uma decisão depende apenas do contexto imediato, não da rede inteira.
    Limitar a profundidade por k saltos (k-hop) previne a explosão
    do uso de memória e corta a exploração inútil.
    
    Complexidade:
    - Tempo: O(b^k)
      Onde 'b' é o fator de ramificação médio (branching factor, os vizinhos) 
      e 'k' é a profundidade limite. Crescimento exponencial restrito apenas
      ao subgrafo próximo.
    - Espaço: O(k)
      Exige muita pouca memória, limitada à profundidade da pilha de recursão.
    
    Args:
        graph (Graph): Instância do grafo a ser explorado.
        start_node (int): Nó de origem inicial.
        target_node (int): Nó de destino desejado.
        k_hop (int): Limite de saltos da busca.
        
    Returns:
        tuple: (caminho_encontrado, tempo_execucao, nos_visitados)
    """
    start_time = time.perf_counter()
    
    # path controla o estado das visitas do caminho de recursão
    path = []
    
    # Utilizando lista como referência para contagem global nas recursões
    visited_count_ref = [0] 
    
    path_found = dls_recursive(graph, start_node, target_node, k_hop, path, visited_count_ref)
    
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    return path_found, execution_time, visited_count_ref[0]
