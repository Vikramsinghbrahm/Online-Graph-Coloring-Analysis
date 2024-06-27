import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for rendering plots

from flask import Flask, request, render_template, jsonify, send_file
from flask_cors import CORS
import networkx as nx
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import matplotlib.pyplot as plt
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


import time

def draw_graph(graph, node_colors=None):
    plt.clf()
    G = nx.Graph(graph)
    pos = nx.spring_layout(G)
    if node_colors is not None:
        colors = [node_colors.get(node, 0) for node in G.nodes()]
        nx.draw(G, pos, node_color=colors, with_labels=True)
    else:
        nx.draw(G, pos, with_labels=True)
    timestamp = int(time.time())
    plt.savefig(f'static/my_plot_{timestamp}.png')
    return timestamp


def random_graph_generator(n, k):
    value = random.random()
    p = value

    subsets = [[] for _ in range(k)]
    for i in range(n):
        subsets[i % k].append(i)

    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if i in subsets[j % k] or j in subsets[i % k]:
                continue
            elif random.random() < p:
                edges.add((i, j))

    graph = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph

def bipartite_is(graph):
    i_set = set()
    i_set2 = set()
    visited = set()

    st_v = len(graph) - 1
    i_set.add(st_v)
    visited.add(st_v)

    qu = [st_v]
    while qu:
        ver = qu.pop(0)
        for neighbor in graph[ver]:
            if neighbor not in visited:
                if ver in i_set:
                    i_set2.add(neighbor)
                else:
                    i_set.add(neighbor)
                visited.add(neighbor)
                qu.append(neighbor)
    return list(i_set), list(i_set2)

def CBIP(G):
    find_minimum_integer = lambda lst: next(i for i in range(1, len(lst) + 2) if i not in set(lst))
    G = nx.Graph(G)
    n = len(G.nodes())
    if n < 1:
        return []
    color_list = [1]
    for i in range(1, n):
        other_part_colors = []
        other_part = bipartite_is(G.subgraph(range(i + 1)))[1]
        for j in other_part:
            other_part_colors.append(color_list[j])
        color = find_minimum_integer(other_part_colors)
        color_list.append(color)
    return color_list

def firstfit(graph):
    colors = {}
    for vertex in graph:
        used_colors = set(colors.get(neighbor) for neighbor in graph[vertex] if neighbor in colors)
        available_colors = set(range(len(graph))) - used_colors
        if available_colors:
            colors[vertex] = min(available_colors)
        else:
            colors[vertex] = len(graph)
    return colors

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
    y = 0

    result = f"Graph coloring using {coloring_method} with k={chromatic_number}, v={num_vertices}, n={num_instances}"

    g1 = []
    c = []
    for i in range(num_instances):
        grap = random_graph_generator(num_vertices, chromatic_number)
        g1 = grap
        if coloring_method == 'cbip':
            x = CBIP(grap)
            unique_values = set(x)
        else:
            x = firstfit(grap)
            unique_values = set(x.values())
        c = x
        y += float((len(unique_values) / chromatic_number))

    Av = y / num_instances

    if coloring_method == 'cbip':
        c = {index: num for index, num in enumerate(c)}
    colormap = c
    node_colors = {node: colormap.get(node, 0) for node in g1.keys()}

    timestamp = draw_graph(g1, node_colors)
    return jsonify({'average': Av, 'image': f'my_plot_{timestamp}.png', 'method': coloring_method})

@app.route('/plot')
def plot():
    return send_file('static/my_plot.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
