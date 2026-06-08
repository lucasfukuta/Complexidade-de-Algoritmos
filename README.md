# Comparação de Desempenho: BFS vs DLS k-hop em Knowledge Graphs Espaciais

Este projeto foi desenvolvido no âmbito académico para a disciplina de **Projeto e Complexidade de Algoritmos (PCA)**. O objetivo principal consiste em analisar, comparar e avaliar a escalabilidade, o consumo de memória e o tempo de execução dos algoritmos de **Busca em Largura (Breadth-First Search - BFS)** e **Busca Limitada por Profundidade (Depth-Limited Search - DLS)** aplicados a *Knowledge Graphs* (KGs) dinâmicos.

O cenário mimetiza ambientes exploratórios de **Aprendizagem por Reforço (Reinforcement Learning - RL)**, onde agentes inteligentes precisam de tomar decisões e planear rotas locais baseadas num horizonte de vizinhança restrito (*k-hop*).

---

## Contexto Académico e Motivação

Em aplicações modernas de Inteligência Artificial e RL, os agentes interagem frequentemente com ambientes representados por grafos de conhecimento (*Knowledge Graphs*). À medida que estes grafos crescem, a varredura completa da rede torna-se proibitiva:

* **O Problema da BFS:** Sendo um algoritmo completo, a BFS explora o grafo de forma uniforme em anéis de profundidade. Embora garanta o caminho mais curto (em número de saltos), a necessidade de manter toda a fronteira de expansão em memória (fila) causa uma explosão do espaço de busca em KGs muito densos, impactando o tempo de inferência do agente.
* **A Solução DLS k-hop:** Ao limitar a profundidade de busca a um número máximo de $k$ saltos, o agente restringe a sua análise apenas ao subgrafo vizinho imediato. Isto elimina a necessidade de armazenar grandes fronteiras e evita explorações inúteis em grafos massivos, tornando o processamento local altamente eficiente.

---

## Modelação Espacial (Topologia de Manhattan)

Para simular o ambiente de um *paper* científico (inspirado na topologia espacial de Stefano), os grafos são gerados procedimentalmente numa **grade bidimensional**. 
* Cada nó (`Entidade_i`) é mapeado para uma coordenada $(x, y)$.
* As conexões (arestas) são restritas estritamente a vizinhos ortogonais diretos (**Vizinhança de Manhattan**).

Esta estrutura simula com precisão o comportamento de movimentação local e as restrições de alcance que um agente inteligente enfrenta no mundo real.


---

## Análise de Complexidade Teórica

| Algoritmo | Complexidade de Tempo (Pior Caso) | Complexidade de Espaço (Pior Caso) | Características |
| :--- | :--- | :--- | :--- |
| **BFS** | $\mathcal{O}(V + E)$ | $\mathcal{O}(V)$ | Garante o caminho mínimo. Elevado pico de memória na fronteira. |
| **DLS $k$-hop** | $\mathcal{O}(b^k)$ | $\mathcal{O}(k)$ | Restrito ao subgrafo local ($b$ é o fator de ramificação). Consumo de memória mínimo (pilha de recursão). |

---

## Estrutura do Projeto

O código está organizado de forma modular, separando a lógica dos algoritmos, a estrutura do grafo e o pipeline de experimentação:

```text
project/
│
├── algorithms/
│   ├── __init__.py
│   ├── bfs.py          # Implementação iterativa do Breadth-First Search com deque
│   └── dls.py          # Implementação recursiva do Depth-Limited Search com Backtracking
│
├── graph/
│   ├── __init__.py
│   ├── graph.py        # Definição das classes base Graph e KnowledgeGraph
│   └── generator.py    # Gerador procedimental de grafos baseados na grade de Manhattan
│
├── experiments/
│   ├── __init__.py
│   └── benchmark.py    # Suite de testes e monitorização de memória (tracemalloc)
│
└── main.py             # Ponto de entrada do programa e introdução académica
```

## Como Executar

O projeto foi desenvolvido utilizando exclusivamente a biblioteca padrão do **Python 3.x**, pelo que não é necessária a instalação de nenhuma dependência externa (como `pip`).

### 1. Execução Completa (Via `main.py`)
Para ver a introdução académica e correr a suite de testes padrão configurada no fluxo principal, basta executar a partir da raiz do projeto:
```bash
python project/main.py
