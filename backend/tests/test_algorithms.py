from graph_coloring.algorithms import cbip_coloring, first_fit_coloring, is_valid_coloring
from graph_coloring.generator import build_partition_map, generate_k_partite_graph


def test_generator_preserves_partitions():
    import random

    rng = random.Random(7)
    graph, partition_map = generate_k_partite_graph(12, 3, rng, edge_probability=1.0)

    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            assert partition_map[vertex] != partition_map[neighbor]


def test_first_fit_returns_valid_coloring():
    graph = {
        0: [1, 2],
        1: [0, 2],
        2: [0, 1],
    }

    coloring = first_fit_coloring(graph)

    assert is_valid_coloring(graph, coloring)
    assert len(set(coloring.values())) == 3


def test_cbip_colors_bipartite_graph_with_two_colors():
    graph = {
        0: [2, 3],
        1: [2],
        2: [0, 1],
        3: [0],
    }

    coloring = cbip_coloring(graph)

    assert is_valid_coloring(graph, coloring)
    assert len(set(coloring.values())) == 2


def test_partition_map_is_balanced():
    partition_map = build_partition_map(8, 3)

    counts = {partition: list(partition_map.values()).count(partition) for partition in set(partition_map.values())}

    assert max(counts.values()) - min(counts.values()) <= 1
