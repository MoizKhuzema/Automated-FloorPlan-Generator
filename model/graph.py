# To import package
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


def create_graph(filename):
    # read file
    df = pd.read_csv(filename)

    # To create an empty undirected graph
    g = nx.Graph()

    # Adding nodes
    for idx in df.index:
        if df['Width'][idx] != 0.0:
            g.add_node(df['Rooms'][idx])
            g.nodes[df['Rooms'][idx]]["Width"] = df['Width'][idx]
            g.nodes[df['Rooms'][idx]]["Height"] = df['Height'][idx]

    # Adding functional presets
    preset = pd.read_csv(r'C:\Users\moizk\Desktop\Upwork\Yafei-Zhou\FloorPlanGenerator\Task_1\functional_preset.csv')
    for idx in preset.index:
        g.add_edge(preset['a'][idx], preset['b'][idx])

    # Adding edges
    edges = pd.read_csv(r'C:\Users\moizk\Desktop\Upwork\Yafei-Zhou\FloorPlanGenerator\Task_1\room_edges.csv', names=['a', 'b'])
    for idx in edges.index:
        if edges['a'][idx] in g.nodes() and edges['b'][idx] in g.nodes():
            g.add_edge(edges['a'][idx], edges['b'][idx])

    return g