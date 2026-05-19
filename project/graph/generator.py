"""
Módulo de geração de grafos alinhados ao paper.
Simula a criação de um Knowledge Graph espacial com vizinhança de Manhattan.
"""
import random
from .graph import KnowledgeGraph

def generate_graph_paper(num_nodes):
    """
    Gera um KnowledgeGraph onde os nós são dispostos em uma grade
    bidimensional e as arestas representam a vizinhança de Manhattan.
    
    Contexto Acadêmico:
    - O grafo simula um Knowledge Graph espacial onde cada nó representa 
      estados, entidades ou conceitos específicos no espaço de estados do agente, 
      e as arestas representam relações de adjacência ou transições possíveis.
    - Isso representa ambientes dinâmicos e complexos porque a estrutura de grade 
      com vizinhos restritos simula o comportamento de movimentação local e de 
      exploração limitada de agentes inteligentes de Reinforcement Learning (RL), 
      onde o agente precisa inferir e planejar localmente sob restrição de alcance (k-hop).
    - Simula a topologia espacial do ambiente do paper do Stefano.
    - Cada nó 'Entidade_i' mapeia para uma coordenada (x, y) na grade.
    - Conectividade restrita a vizinhos ortogonais diretos (vizinhos de Manhattan).
    
    Args:
        num_nodes (int): Número total de nós a serem gerados.
        
    Returns:
        KnowledgeGraph: O grafo espacial gerado.
    """
    kg = KnowledgeGraph()
    
    if num_nodes <= 0:
        return kg
        
    # Simula o tamanho de uma grade baseada no número de nós
    # Ex: 10.000 nós correspondem a uma grade de 100x100
    grid_size = int(num_nodes ** 0.5)
    if grid_size == 0:
        grid_size = 1
    
    # 1. Criar nós com posições espaciais
    for i in range(num_nodes):
        node_id = f"Entidade_{i}"
        # Mapeia o ID linear para uma coordenada (x, y) na grade
        x = i // grid_size
        y = i % grid_size
        kg.adicionar_no(node_id, x, y)
        
    # 2. Criar arestas respeitando a vizinhança de Manhattan (Manhattan Neighbours)
    for i in range(num_nodes):
        node_id = f"Entidade_{i}"
        x = i // grid_size
        y = i % grid_size
        
        # Vizinhos ortogonais possíveis na grade (Norte, Sul, Leste, Oeste)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                neighbor_idx = nx * grid_size + ny
                if neighbor_idx < num_nodes:
                    neighbor_id = f"Entidade_{neighbor_idx}"
                    kg.adicionar_aresta(node_id, neighbor_id)
                    
    return kg

def generate_graph(num_nodes, edges_per_node=None):
    """
    Wrapper de compatibilidade para a suite de benchmarks existente.
    """
    return generate_graph_paper(num_nodes)

