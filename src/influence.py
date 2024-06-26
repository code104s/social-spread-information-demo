import numpy as np


# Tinh danh sach cac
def influence_count(nodes, edges, seeds, threshold):
    ''' Calculate influent result
    Args:
        nodes (list) [#node]: nodes list of the graph;
        edges (list of list) [#edge, 2]: edges list of the graph;
        seeds (list) [#seed]: selected seeds;
        threshold (float): influent threshold, between 0 and 1;
    Return:
        final_actived_node (list): list of influent nodes;
        edge_probs (dict): dictionary of edge probabilities;
    '''
    in_degree = {}
    inactive_nodes = []
    active_nodes = []
    nodes_status = {}
    edge_probs = {}  # new dictionary to store edge probabilities

    for edge in edges:
        if edge[0] in seeds:
            active_nodes.append(edge[0])
        else:
            inactive_nodes.append(edge[0])
        if edge[1] in seeds:
            active_nodes.append(edge[1])
        else:
            inactive_nodes.append(edge[1])
        if edge[1] in in_degree:
            in_degree[edge[1]] += 1
        else:
            in_degree[edge[1]] = 1
        edge_probs[(edge[0], edge[1])] = threshold / in_degree[edge[1]]  # store the edge probability

    active_nodes = list(set(active_nodes))
    inactive_nodes = list(set(inactive_nodes))

    for node in nodes:
        nodes_status[node] = 0
    for node in active_nodes:
        nodes_status[node] = 1

    while active_nodes:
        new_actived_nodes = []
        for edge in edges:
            if nodes_status[edge[0]] == 1:
                if nodes_status[edge[1]] == 0:
                    p = np.array([1 - threshold / in_degree[edge[1]], threshold / in_degree[edge[1]]])
                    flag = np.random.choice([0, 1], p=p.ravel()) # trả về 0 (không thành công) hoặc 1 (thành công)
                    if flag:
                        new_actived_nodes.append(edge[1])
        for node in active_nodes:
            nodes_status[node] = 2
        for node in new_actived_nodes:
            nodes_status[node] = 1
        active_nodes = new_actived_nodes

    final_actived_node = [node for node in nodes if nodes_status[node] == 2]
    return final_actived_node, edge_probs


# Tính độ phủ
def coverage(nodes, final_actived_node):
    ''' Calculate coverage
    Args:
        nodes (list) [#node]: nodes list of the graph;
        final_actived_node (int): number of final active nodes;
    Return:
        coverage (float): coverage of the influence;
    '''
    coverage = final_actived_node / len(nodes)
    return coverage


def precision(true_positives, predicted_positives):
    ''' Calculate precision
    Args:
        true_positives (int): number of true positive results;
        predicted_positives (int): number of predicted positive results;
    Return:
        precision (float): precision of the influence;
    '''
    if predicted_positives == 0:
        return 0
    else:
        return true_positives / predicted_positives
