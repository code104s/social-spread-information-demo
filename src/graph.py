import tkinter as tk

import networkx as nx
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random


class GraphWindow(tk.Toplevel):
    def __init__(self, master=None, nodes=None, edges=None, seeds=None, max_nodes=13):
        super().__init__(master)
        self.title("Graph Window")
        self.create_graph(nodes, edges, seeds, max_nodes)
        self.mainloop()  # Start the event loop

    def create_graph(self, nodes, edges, seeds, max_nodes):
        G = nx.DiGraph()

        # Tạo một đồ thị đầy đủ từ tất cả các nút và cạnh
        full_graph = nx.DiGraph()
        full_graph.add_nodes_from(nodes)
        full_graph.add_edges_from(edges)

        # Chọn một seed ngẫu nhiên
        seed = random.choice(seeds)

        # Tìm tất cả các nút liền kề với seed
        adjacent_nodes = list(full_graph.neighbors(seed))

        # Giới hạn số lượng nút để vẽ
        if len(adjacent_nodes) > max_nodes - 1:
            adjacent_nodes = adjacent_nodes[:max_nodes - 1]

        # Vẽ seed và các nút liền kề
        nodes_to_draw = [seed] + adjacent_nodes

        # Vẽ các nodes và edges
        for node in nodes_to_draw:
            if node == seed:
                continue  # Skip the seed for now
            else:
                G.add_node(node, color='blue')

        # Now add the seed
        G.add_node(seed, color='red')

        for edge in edges:
            if edge[0] in nodes_to_draw and edge[1] in nodes_to_draw:
                G.add_edge(*edge)

        pos = nx.spring_layout(G)

        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot(111)

        # Vẽ các nút và cạnh theo màu
        non_seed_nodes = [node for node in G.nodes() if node != seed]
        seed_nodes = [node for node in G.nodes() if node == seed]

        nx.draw_networkx_edges(G, pos, ax=ax)

        for node in non_seed_nodes:
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='blue', ax=ax)

        for node in seed_nodes:
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='red', ax=ax)

        nx.draw_networkx_labels(G, pos, ax=ax)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


class GraphWindow2(tk.Toplevel):
    def __init__(self, master=None, nodes=None, edges=None, seeds=None):
        super().__init__(master)
        self.title("Graph Window")
        self.create_graph(nodes, edges, seeds)
        self.mainloop()  # Start the event loop

    def create_graph(self, nodes, edges, seeds):
        G = nx.DiGraph()

        # Add all nodes and edges to the graph
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        pos = nx.spring_layout(G)

        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot(111)

        # Draw all nodes and edges
        non_seed_nodes = [node for node in G.nodes() if node not in seeds]
        seed_nodes = [node for node in G.nodes() if node in seeds]

        nx.draw_networkx_edges(G, pos, ax=ax, arrows=True)

        for node in non_seed_nodes:
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='blue', ax=ax)

        for node in seed_nodes:
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='red', ax=ax)

        nx.draw_networkx_labels(G, pos, ax=ax)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
