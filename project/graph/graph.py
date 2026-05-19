"""
Módulo de definição da estrutura do Grafo.
Representa um Knowledge Graph dinâmico utilizando lista de adjacências.
"""

class Graph:
    def __init__(self):
        """
        Inicializa um novo grafo vazio.
        Utiliza um dicionário (adj_list) para armazenar as listas de adjacência,
        onde as chaves são os nós e os valores são listas de nós vizinhos.
        """
        self.adj_list = {}
        self.num_edges = 0

    def add_node(self, node):
        """
        Adiciona um novo nó ao grafo, caso ainda não exista.
        """
        if node not in self.adj_list:
            self.adj_list[node] = []

    def add_edge(self, u, v):
        """
        Adiciona uma aresta não direcionada entre os nós u e v.
        Ambos os nós são criados caso não existam no grafo.
        """
        self.add_node(u)
        self.add_node(v)
        
        # Previne arestas duplicadas
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)
            self.num_edges += 1

    def get_neighbors(self, node):
        """
        Retorna a lista de vizinhos de um determinado nó.
        """
        return self.adj_list.get(node, [])

    def get_num_nodes(self):
        """
        Retorna a quantidade total de nós presentes no grafo.
        """
        return len(self.adj_list)

    def get_num_edges(self):
        """
        Retorna a quantidade total de arestas presentes no grafo.
        """
        return self.num_edges

    def print_statistics(self):
        """
        Imprime as estatísticas gerais do grafo (nós e arestas).
        """
        print("=== Estatísticas do Grafo ===")
        print(f"Total de Nós: {self.get_num_nodes()}")
        print(f"Total de Arestas: {self.get_num_edges()}")
        print("=============================")


class KnowledgeGraph(Graph):
    def __init__(self):
        super().__init__()
        self.positions = {}

    def adicionar_no(self, node_id, x, y):
        """
        Adiciona um nó ao grafo com coordenadas espaciais (x, y).
        """
        self.add_node(node_id)
        self.positions[node_id] = (x, y)

    def adicionar_aresta(self, u, v):
        """
        Adiciona uma aresta não direcionada entre os nós u e v.
        """
        self.add_edge(u, v)

