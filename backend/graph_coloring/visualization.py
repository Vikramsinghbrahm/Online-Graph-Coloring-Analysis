from pathlib import Path
from uuid import uuid4

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx

Graph = dict[int, list[int]]
Coloring = dict[int, int]


def render_graph_image(graph: Graph, coloring: Coloring, output_dir: Path) -> str:
    output_dir.mkdir(parents=True, exist_ok=True)

    network = nx.Graph()
    for vertex, neighbors in graph.items():
        network.add_node(vertex)
        for neighbor in neighbors:
            if vertex < neighbor:
                network.add_edge(vertex, neighbor)

    figure, axis = plt.subplots(figsize=(7.5, 5.5))
    positions = nx.spring_layout(network, seed=42)
    node_colors = [coloring.get(vertex, 0) for vertex in network.nodes]

    nx.draw_networkx(
        network,
        pos=positions,
        node_color=node_colors,
        cmap=plt.cm.Set3,
        with_labels=True,
        font_size=9,
        node_size=850,
        edgecolors="#243b53",
        linewidths=1.2,
        ax=axis,
    )

    axis.set_axis_off()
    figure.tight_layout()

    image_name = f"graph_{uuid4().hex[:10]}.png"
    figure.savefig(output_dir / image_name, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return image_name
