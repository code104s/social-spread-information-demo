import tkinter as tk
import src.seed as seed
from src.data import data_load
from src.influence import influence_count, coverage, precision
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.init_rate_label = tk.Label(self, text="Initial Rate (0 to 0.05):")
        self.init_rate_label.pack()
        self.init_rate_entry = tk.Entry(self)
        self.init_rate_entry.pack()

        self.threshold_label = tk.Label(self, text="Influence Threshold (0 to 1):")
        self.threshold_label.pack()
        self.threshold_entry = tk.Entry(self)
        self.threshold_entry.pack()

        self.calculate_button = tk.Button(self)
        self.calculate_button["text"] = "Calculate"
        self.calculate_button["command"] = self.calculate_and_display_results
        self.calculate_button.pack()

        self.result_text = tk.Text(self)
        self.result_text.pack()

    def calculate_and_display_results(self):
        init_rate = float(self.init_rate_entry.get())
        threshold = float(self.threshold_entry.get())

        # Parameters
        path = '../data/example.txt'  # dataset file path
        policy = 'mia'  # Seed selection policy

        # Seed selection
        nodes, edges = data_load(path)
        seeds_number = int(len(nodes) * init_rate)

        if policy == 'mia':
            seeds = seed.mia(nodes, edges, seeds_number)
        else:
            raise NameError("Unknown policy")

        # Calculate final influence number
        influence_number = influence_count(nodes, edges, seeds, threshold)

        # Calculate coverage
        coverage_result = coverage(nodes, influence_number)

        # Calculate precision
        predicted_positives = len(seeds)
        true_positives = influence_number
        precision_result = precision(true_positives, predicted_positives)

        # Display results
        result = f"Final Influence Number: {influence_number}\n" \
                 f"Coverage: {coverage_result}\n" \
                 f"Precision: {precision_result}"
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

        # Draw graph
        self.draw_graph(nodes, edges, seeds)

    def draw_graph(self, nodes, edges, seeds):
        G = nx.Graph()

        # Add nodes
        for node in nodes:
            if node in seeds:
                G.add_node(node, color='red')  # color seeds in red
            else:
                G.add_node(node, color='blue')  # color other nodes in blue

        # Add edges
        for edge in edges:
            G.add_edge(*edge)

        colors = [node[1]['color'] for node in G.nodes(data=True)]

        # Create figure and draw the graph
        fig = plt.Figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        nx.draw(G, with_labels=True, node_color=colors, ax=ax)

        # Create a tkinter Canvas to display the figure
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

root = tk.Tk()
app = Application(master=root)
app.mainloop()