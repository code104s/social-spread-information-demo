import random
import tkinter as tk
from tkinter import ttk

import pandas as pd

import src.seed as seed
from src.graph import GraphWindow2
from src.influence import influence_count, coverage, precision


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def load_csv_data(path):
        '''Load data from a CSV file
        Args:
            path (str): path to the CSV file;
        Return:
            df (DataFrame): DataFrame of the CSV file data;
        '''
        df = pd.read_csv(path, sep=';')
        return df

    def create_widgets(self):
        self.init_rate_label = tk.Label(self, text="Initial Rate (0 to 1):")
        self.init_rate_label.grid(row=0, column=0)
        self.init_rate_entry = tk.Entry(self)
        self.init_rate_entry.grid(row=1, column=0)

        self.threshold_label = tk.Label(self, text="Influence Threshold (0 to 1):")
        self.threshold_label.grid(row=2, column=0)
        self.threshold_entry = tk.Entry(self)
        self.threshold_entry.grid(row=3, column=0)

        self.num_nodes_label = tk.Label(self, text="Number of Nodes:")
        self.num_nodes_label.grid(row=4, column=0)
        self.num_nodes_entry = tk.Entry(self)
        self.num_nodes_entry.grid(row=5, column=0)

        self.calculate_with_data_button = tk.Button(self, text="Calculate with Data", command=self.calculate_with_data)
        self.calculate_with_data_button.grid(row=7, column=0)

        # Load data from CSV file
        self.df = pd.read_csv('../data/Earthquake - Metadata.csv', sep=';')
        # Get list of article titles
        article_titles = self.df['Article Title'].tolist()

        # Create a Combobox with the article titles
        self.article_title_label = tk.Label(self, text="Spread:")
        self.article_title_label.grid(row=0, column=1)
        self.article_title_combobox = ttk.Combobox(self, values=article_titles, width=50)
        self.article_title_combobox.grid(row=1, column=1)
        self.article_title_combobox.bind("<<ComboboxSelected>>", self.update_additional_info)

        # Create labels to display additional info
        self.language_id_label = tk.Label(self, text="")
        self.language_id_label.grid(row=2, column=1)
        self.event_label = tk.Label(self, text="")
        self.event_label.grid(row=3, column=1)
        self.weight_label = tk.Label(self, text="")
        self.weight_label.grid(row=4, column=1)

        # Add a new button for calculating with weight
        self.calculate_with_weight_button = tk.Button(self, text="Use Weight for Threshold", command=self.calculate_with_weight)
        self.calculate_with_weight_button.grid(row=7, column=1)

        # Add a new checkbox for deciding whether to draw edge labels
        self.draw_edge_labels_var = tk.IntVar()
        self.draw_edge_labels_checkbox = tk.Checkbutton(self, text="Draw Edge Labels", variable=self.draw_edge_labels_var)
        self.draw_edge_labels_checkbox.grid(row=6, column=1)

        # Add a new button for clearing result_text
        self.clear_result_text_button = tk.Button(self, text="Clear Result", command=self.clear_result_text)
        self.clear_result_text_button.grid(row=9, column=0)

        self.result_text = tk.Text(self)
        self.result_text.grid(row=8, column=0, columnspan=2)

    def update_additional_info(self, event):
        # Get selected article title
        selected_title = self.article_title_combobox.get()

        # Find the row in the DataFrame that corresponds to the selected article title
        row = self.df[self.df['Article Title'] == selected_title]

        # Get the values of 'Language+ID', 'Event' and 'Weight'
        language_id = row['Lanaguage+ID'].values[0]
        event = row['Event'].values[0]
        weight = row['Weight'].values[0]

        # Update the labels to display these values
        self.language_id_label.config(text=f"Language+ID: {language_id}")
        self.event_label.config(text=f"Event: {event}")
        self.weight_label.config(text=f"Weight: {weight}")
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

        try:
            num_nodes = int(self.num_nodes_entry.get())
            if num_nodes <= 0:
                raise ValueError("Number of Nodes must be greater than 0.")
        except ValueError:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Invalid Number of Nodes. Please enter a positive integer.")
            return

        try:
            init_rate = float(self.init_rate_entry.get())
            if not (0 <= init_rate <= 1):
                raise ValueError("Initial Rate must be between 0 and 1.")
        except ValueError:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Invalid Initial Rate. Please enter a number between 0 and 0.05.")
            return

        try:
            threshold = float(self.threshold_entry.get())
            if not (0 <= threshold <= 1):
                raise ValueError("Influence Threshold must be between 0 and 1.")
        except ValueError:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Invalid Influence Threshold. Please enter a number between 0 and 1.")
            return

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

        # Get the state of the checkbox
        draw_edge_labels = bool(self.draw_edge_labels_var.get())

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

        # Create legend text
        legend_text = "\n\nNote:\nRed: Seed Nodes\nGreen: Activated Nodes\nBlue: Other Nodes"

        # Add legend text to result
        result += legend_text
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

        # Draw graph with all nodes
        nodes_to_draw = nodes
        GraphWindow2(self.master, nodes, edges, seeds, final_actived_node, edge_probs=edge_probs, draw_edge_labels=draw_edge_labels)

    def calculate_with_weight(self):
        # Get selected article title
        selected_title = self.article_title_combobox.get()

        # Find the row in the DataFrame that corresponds to the selected article title
        row = self.df[self.df['Article Title'] == selected_title]

        # Get the weight value
        weight = row['Weight'].values[0]

        # Use the weight value as the threshold for the calculation
        self.threshold_entry.delete(0, tk.END)
        self.threshold_entry.insert(0, str(weight))

        # Call the calculate_with_data method to perform the calculation
        self.calculate_with_data()

    def clear_result_text(self):
        # Clear the result_text widget
        self.result_text.delete(1.0, tk.END)
    # def recalculate(self):
    #     # Clear the result text box
    #     self.result_text.delete(1.0, tk.END)
    #
    #     # Call calculate_with_data to perform the calculations and display the new results
    #     self.calculate_with_data()
    #
    #     # Draw graph with all nodes
    #     nodes_to_draw = self.nodes
    #     GraphWindow2(self.master, self.nodes, self.edges, self.seeds, self.final_actived_node, edge_probs=self.edge_probs)



root = tk.Tk()
app = Application(master=root)
app.mainloop()
