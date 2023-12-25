from aocd.models import Puzzle
import networkx as nx

puzzle = Puzzle(year=2023, day=25)

lines = puzzle.input_data.splitlines()

G = nx.Graph()

for line in lines:
    p1, p2 = line.split(":")
    node = p1
    for neigh in p2.split(" "):
        neigh = neigh.strip()
        if neigh:
            G.add_edge(node, neigh)

# Min cut to split the graph
cuts = nx.minimum_edge_cut(G)
G.remove_edges_from(cuts)

subgraphs = list(nx.connected_components(G))

puzzle.answer_a = len(subgraphs[0]) * len(subgraphs[1])
