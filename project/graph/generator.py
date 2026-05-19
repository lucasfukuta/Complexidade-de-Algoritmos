"""
Módulo de geração de grafos aleatórios.
Simula a criação de um Knowledge Graph que pode representar
um ambiente dinâmico de Reinforcement Learning.
"""
import random
from .graph import Graph

def generate_graph(num_nodes, edges_per_node):
    """
    Gera um grafo conectado aleatório.
    
    Contexto Acadêmico:
    - O grafo simula um Knowledge Graph onde nós representam estados,
      entidades ou conceitos, e as arestas representam transições ou relações.
    - Isso representa ambientes dinâmicos e complexos porque a geração
      aleatória com conectividade variável imita a imprevisibilidade e 
      a topologia de domínios abertos de Reinforcement Learning, onde agentes
      inteligentes não conhecem toda a estrutura antecipadamente e precisam
      explorar subgrafos para tomar decisões.
    
    Args:
        num_nodes (int): Quantidade de nós a serem gerados no grafo.
        edges_per_node (int): Fator de densidade que influencia o número total de arestas.
    
    Returns:
        Graph: O objeto grafo gerado.
    """
    g = Graph()
    
    if num_nodes <= 0:
        return g
        
    # Adiciona nós base usando inteiros (0 até num_nodes - 1)
    for i in range(num_nodes):
        g.add_node(i)
        
    # Garantir que o grafo seja completamente conectado (sem ilhas)
    # Criamos uma árvore geradora básica ligando todos os nós em um caminho embaralhado
    nodes = list(range(num_nodes))
    random.shuffle(nodes)
    for i in range(len(nodes) - 1):
        g.add_edge(nodes[i], nodes[i+1])
        
    # Calcular quantas arestas faltam para atingir a densidade desejada
    # Uma árvore geradora tem num_nodes - 1 arestas
    target_edges = (num_nodes * edges_per_node) // 2
    current_edges = g.get_num_edges()
    
    attempts = 0
    # Limite máximo para evitar loops infinitos caso o grafo atinja a capacidade máxima de arestas
    max_attempts = num_nodes * edges_per_node * 5 
    
    # Adicionar nós aleatoriamente até atingir a densidade (cada nó terá múltiplos vizinhos)
    while current_edges < target_edges and attempts < max_attempts:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        
        # Evitar auto-loops e checar se aresta já existe
        if u != v and v not in g.get_neighbors(u):
            g.add_edge(u, v)
            current_edges += 1
        
        attempts += 1
            
    return g
