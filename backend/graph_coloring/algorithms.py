from collections import deque

Graph = dict[int, list[int]]
Coloring = dict[int, int]


def _smallest_available_color(used_colors: set[int]) -> int:
    color = 1
    while color in used_colors:
        color += 1
    return color


def first_fit_coloring(graph: Graph) -> Coloring:
    coloring: Coloring = {}

    for vertex in sorted(graph):
        used_colors = {coloring[neighbor] for neighbor in graph[vertex] if neighbor in coloring}
        coloring[vertex] = _smallest_available_color(used_colors)

    return coloring


def _induced_subgraph(graph: Graph, vertices: list[int], vertex_set: set[int]) -> Graph:
    return {
        vertex: [neighbor for neighbor in graph[vertex] if neighbor in vertex_set]
        for vertex in vertices
    }


def _opposite_partition(prefix_graph: Graph, start_vertex: int) -> set[int]:
    queue: deque[int] = deque([start_vertex])
    parity = {start_vertex: 0}

    while queue:
        vertex = queue.popleft()
        for neighbor in prefix_graph[vertex]:
            expected_parity = 1 - parity[vertex]
            if neighbor not in parity:
                parity[neighbor] = expected_parity
                queue.append(neighbor)
                continue

            if parity[neighbor] != expected_parity:
                raise ValueError("CBIP requires a bipartite graph.")

    return {vertex for vertex, partition in parity.items() if partition == 1}


def cbip_coloring(graph: Graph) -> Coloring:
    coloring: Coloring = {}
    revealed_vertices: list[int] = []
    revealed_set: set[int] = set()

    for vertex in sorted(graph):
        revealed_vertices.append(vertex)
        revealed_set.add(vertex)

        prefix_graph = _induced_subgraph(graph, revealed_vertices, revealed_set)
        opposite_partition = _opposite_partition(prefix_graph, vertex)
        used_colors = {coloring[other_vertex] for other_vertex in opposite_partition if other_vertex in coloring}
        coloring[vertex] = _smallest_available_color(used_colors)

    return coloring


def color_graph(graph: Graph, method: str) -> Coloring:
    if method == "cbip":
        return cbip_coloring(graph)
    if method == "first_fit":
        return first_fit_coloring(graph)
    raise ValueError(f"Unsupported coloring method: {method}")


def is_valid_coloring(graph: Graph, coloring: Coloring) -> bool:
    for vertex, neighbors in graph.items():
        vertex_color = coloring.get(vertex)
        if vertex_color is None:
            return False

        for neighbor in neighbors:
            if vertex_color == coloring.get(neighbor):
                return False

    return True
