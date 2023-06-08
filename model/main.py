# To import package
import networkx as nx
import matplotlib.pyplot as plt
from graph import create_graph
from plot import plot
from layout_2 import generate_layout
from edges import traverse_edge
from render import render


if __name__ == '__main__':
    # max dimensions
    width = 1500
    height = 1500

    # read file
    filename = r'C:\Users\moizk\Desktop\Upwork\Yafei-Zhou\Hybrid-model\Results\exp-1\room_sizes.csv'
    G = create_graph(filename)

    rects, dinner_flag= generate_layout(G, width, height)
    label = []
    for r in rects:
        label.append(r['label'])
    
    rects = traverse_edge('doors_2.csv', rects, label, dinner_flag)
    render(width, height, rects)

    # Plot rects
    # plot(rects, width, height, label= label)s
    # plt.show()

    # Draw graph
    # nx.draw(G, with_labels=True)
    # plt.show()