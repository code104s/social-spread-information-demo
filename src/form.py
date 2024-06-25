import tkinter as tk

import networkx as nx
import seed
import self

import src.seed as seed
from src import graph
from src.data import data_load
from src.influence import influence_count, coverage, precision
import random
from src.graph import GraphWindow, GraphWindow2


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

        # self.calculate_button = tk.Button(self)
        # self.calculate_button["text"] = "Calculate"
        # self.calculate_button["command"] = self.calculate_and_display_results
        # self.calculate_button.pack()

        self.num_nodes_label = tk.Label(self, text="Number of Nodes:")
        self.num_nodes_label.pack()
        self.num_nodes_entry = tk.Entry(self)
        self.num_nodes_entry.pack()

        self.calculate_with_data_button = tk.Button(self)
        self.calculate_with_data_button["text"] = "Calculate with Data"
        self.calculate_with_data_button["command"] = self.calculate_with_data
        self.calculate_with_data_button.pack()

        self.result_text = tk.Text(self)
        self.result_text.pack()

    # def calculate_and_display_results(self):
    #     init_rate = float(self.init_rate_entry.get())
    #     threshold = float(self.threshold_entry.get())
    #
    #     # Parameters
    #     path = '../data/example.txt'  # dataset file path
    #     policy = 'mia'  # Seed selection policy
    #
    #     # Seed selection
    #     nodes, edges = data_load(path)
    #     seeds_number = int(len(nodes) * init_rate)
    #
    #     if policy == 'mia':
    #         seeds = seed.mia(nodes, edges, seeds_number)
    #     else:
    #         raise NameError("Unknown policy")
    #
    #     # Calculate final influence number
    #     influence_number = influence_count(nodes, edges, seeds, threshold)
    #
    #     # Calculate coverage
    #
    #     coverage_result = coverage(nodes, len(influence_number))  #Calculate precision
    #     predicted_positives = len(seeds)
    #     true_positives = influence_number
    #     precision_result = precision(true_positives, predicted_positives)
    #
    #     # Display results
    #     result = f"Final Influence Number: {influence_number}\n" \
    #              f"Coverage: {coverage_result}\n" \
    #              f"Precision: {precision_result}" \
    #              f"\n\nSelected seeds: {seeds}"
    #     self.result_text.delete(1.0, tk.END)
    #     self.result_text.insert(tk.END, result)
    #
    #     # Draw graph
    #     GraphWindow(self.master, nodes, edges, seeds)

    def calculate_with_data(self):
        num_nodes = int(self.num_nodes_entry.get())
        # Generate nodes and edges based on num_nodes
        nodes = list(range(1, num_nodes + 1))
        edges = []
        for _ in range(num_nodes * 2):  # Generate 2 * num_nodes edges
            node1, node2 = random.sample(nodes, 2)
            edges.append((node1, node2))

        init_rate = float(self.init_rate_entry.get())
        threshold = float(self.threshold_entry.get())

        # Parameters
        policy = 'mia'  # Seed selection policy

        # Seed selection
        seeds_number = int(len(nodes) * init_rate)

        if policy == 'mia':
            seeds = seed.mia(nodes, edges, seeds_number, threshold)
        else:
            raise NameError("Unknown policy")

        # Calculate final influence number
        final_actived_node, edge_probs = influence_count(nodes, edges, seeds, threshold)

        # Calculate coverage
        coverage_result = coverage(nodes, len(final_actived_node))

        # Calculate precision
        predicted_positives = len(seeds)
        true_positives = len(final_actived_node)
        precision_result = precision(true_positives, predicted_positives)

        paths = []
        paths_text = "\n".join(" -> ".join(str(node) for node in path) for path in paths)

        # Display results
        result = f"Final Influence Number: {len(final_actived_node)}\n" \
                 f"Coverage: {coverage_result}\n" \
                 f"Precision: {precision_result}" \
                 f"\n\nSelected seeds: {seeds}" \
                 f"\n\nPaths:\n{paths_text}"
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

        # Draw graph with all nodes
        nodes_to_draw = nodes
        GraphWindow2(self.master, nodes, edges, seeds, final_actived_node, edge_probs=edge_probs)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
