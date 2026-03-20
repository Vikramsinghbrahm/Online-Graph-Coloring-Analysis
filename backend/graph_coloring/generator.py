import random

Graph = dict[int, list[int]]


def build_partition_map(num_vertices: int, partition_count: int) -> dict[int, int]:
    return {vertex: vertex % partition_count for vertex in range(num_vertices)}


def generate_k_partite_graph(
    num_vertices: int,
    partition_count: int,
    rng: random.Random,
    edge_probability: float,
) -> tuple[Graph, dict[int, int]]:
    partition_map = build_partition_map(num_vertices, partition_count)
    graph = {vertex: [] for vertex in range(num_vertices)}

    for left in range(num_vertices):
        for right in range(left + 1, num_vertices):
            if partition_map[left] == partition_map[right]:
                continue

            if rng.random() <= edge_probability:
                graph[left].append(right)
                graph[right].append(left)

    return graph, partition_map
