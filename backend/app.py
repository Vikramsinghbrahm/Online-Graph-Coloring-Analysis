import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for rendering plots

from flask import Flask, request, render_template, jsonify, send_file
from flask_cors import CORS
import networkx as nx
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import random
import time

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

def generate_random_graph(num_vertices, chromatic_number):
    """Generate a random graph."""
    p = random.random()
    subsets = [[] for _ in range(chromatic_number)]
    for i in range(num_vertices):
        subsets[i % chromatic_number].append(i)

    edges = set()
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if i in subsets[j % chromatic_number] or j in subsets[i % chromatic_number]:
                continue
            elif random.random() < p:
                edges.add((i, j))

    graph = {i: [] for i in range(num_vertices)}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph

def find_bipartite_sets(graph):
    """Find bipartite independent sets."""
    set1, set2, visited = set(), set(), set()
    start_vertex = len(graph) - 1
    set1.add(start_vertex)
    visited.add(start_vertex)
    queue = [start_vertex]

    while queue:
        vertex = queue.pop(0)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                if vertex in set1:
                    set2.add(neighbor)
                else:
                    set1.add(neighbor)
                visited.add(neighbor)
                queue.append(neighbor)
    return list(set1), list(set2)

def color_with_cbip(graph):
    """Color the graph using CBIP algorithm."""
    def find_minimum_integer(used_colors):
        for i in range(1, len(used_colors) + 2):
            if i not in used_colors:
                return i

    G = nx.Graph(graph)
    color_list = [1]
    for i in range(1, len(G.nodes)):
        other_part_colors = []
        other_part = find_bipartite_sets(G.subgraph(range(i + 1)))[1]
        for j in other_part:
            other_part_colors.append(color_list[j])
        color = find_minimum_integer(other_part_colors)
        color_list.append(color)
    return color_list

def color_with_first_fit(graph):
    """Color the graph using First Fit algorithm."""
    colors = {}
    for vertex in graph:
        used_colors = {colors[neighbor] for neighbor in graph[vertex] if neighbor in colors}
        available_colors = set(range(len(graph))) - used_colors
        colors[vertex] = min(available_colors) if available_colors else len(graph)
    return colors

def draw_graph(graph, node_colors=None):
    """Draw the graph and save it as an image."""
    plt.clf()
    G = nx.Graph(graph)
    pos = nx.spring_layout(G)
    colors = [node_colors.get(node, 0) for node in G.nodes()] if node_colors else None
    nx.draw(G, pos, node_color=colors, with_labels=True)
    timestamp = int(time.time())
    plt.savefig(f'static/graph_{timestamp}.png')
    return timestamp

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/graph-coloring', methods=['POST'])
def graph_coloring():
    data = request.json
    chromatic_number = int(data['chromaticNumber'])
    num_vertices = int(data['numberOfVertices'])
    num_instances = int(data['numberOfInstances'])
    coloring_method = data['coloringMethod']
    total_ratio = 0

    for _ in range(num_instances):
        graph = generate_random_graph(num_vertices, chromatic_number)
        if coloring_method == 'cbip':
            colors = color_with_cbip(graph)
            unique_colors = set(colors)
        else:
            colors = color_with_first_fit(graph)
            unique_colors = set(colors.values())
        total_ratio += len(unique_colors) / chromatic_number

    average_ratio = total_ratio / num_instances

    node_colors = {index: color for index, color in enumerate(colors)}
    timestamp = draw_graph(graph, node_colors)

    return jsonify({'average': average_ratio, 'image': f'graph_{timestamp}.png', 'method': coloring_method})

@app.route('/plot')
def plot():
    return send_file('static/my_plot.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
