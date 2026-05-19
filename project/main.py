"""
Arquivo principal de execução.
Orquestra o projeto de Projeto e Complexidade de Algoritmos (PCA).
"""
import sys
import os

# Adiciona o diretório base no path para importar corretamente caso executado de outro canto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from experiments.benchmark import run_benchmark

def print_introduction():
    """
    Exibe a introdução acadêmica do trabalho.
    """
    print("\n" + "=" * 75)
    print(" PROJETO ACADÊMICO: COMPARAÇÃO BFS vs DLS K-HOP EM KNOWLEDGE GRAPHS ")
    print("=" * 75)
    print("\n[OBJETIVO DO PROJETO]")
    print("Comparar o desempenho, complexidade de tempo/espaço e escalabilidade")
    print("entre os algoritmos BFS (Breadth-First Search) e DLS (Depth-Limited Search)")
    print("quando aplicados em subgrafos de Knowledge Graphs dinâmicos, um cenário")
    print("altamente inspirado em ambientes exploratórios de Reinforcement Learning.\n")
    
    print("[CONTEXTO ACADÊMICO E TEÓRICO]")
    print("- Agentes Inteligentes em RL precisam tomar decisões explorando os grafos")
    print("  de forma constante. O custo de varredura afeta os tempos de inferência.")
    print("- O BFS faz uma exploração robusta de vizinhança e é completo, no entanto,")
    print("  gera altos custos computacionais ao varrer todo o Knowledge Graph, lidando")
    print("  com explosões do espaço de busca.")
    print("- O DLS k-hop propõe uma restrição de horizonte de busca: ao limitar a")
    print("  profundidade (k), o agente avalia apenas o subgrafo vizinho imediato.")
    print("  Isso permite processamento eficiente em grafos massivos.\n")
    print("=" * 75 + "\n")

def main():
    """
    Ponto de entrada do programa principal.
    """
    try:
        print_introduction()
        print("Iniciando a geração de grafos e execução dos Benchmarks...\n")
        
        # Chama as rotinas de experimentos modulares
        run_benchmark()
        
        print("\n[SUCESSO] Todos os benchmarks experimentais foram concluídos.")
    except KeyboardInterrupt:
        print("\n[AVISO] Execução interrompida pelo usuário.")
    except Exception as e:
        print(f"\n[ERRO FATAL] Ocorreu um erro durante a execução: {e}")

if __name__ == "__main__":
    main()
