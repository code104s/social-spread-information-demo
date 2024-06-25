import numpy as np
import heapq


def shortest_path(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return distances


def mia(nodes, edges, n):
    ''' select seeds by mia policy
    args:
        nodes (list) [#node]: node list of the graph;
        edges (list of list) [#edge, 2]: edge list of the graph;
        n (int): number of seeds;
    returns:
        seeds: (list) [#seed]: selected seed nodes index;
    '''
    out_connection = {} # số lượng cạnh ra của mỗi node
    in_connection = {} # số lượng cạnh vào của mỗi node
    centrality_score = {}
    seeds = []
    for edge in edges:
        if edge[0] in out_connection:
            out_connection[edge[0]].append(edge[1])
        else:
            out_connection[edge[0]] = [edge[1]]
        if edge[1] in in_connection:
            in_connection[edge[1]] += 1
        else:
            in_connection[edge[1]] = 1
    for node in nodes:
        centrality_score[node] = mia_centrality(node, out_connection, in_connection)
    i = 0
    for node, _ in sorted(centrality_score.items(), key=lambda item: item[1], reverse=True):
        if i >= n:
            break
        else:
            i += 1
        seeds.append(node)
    return seeds


def mia_centrality(node, out_connection, in_connection):
    ''' select seeds by mia centrality policy
    '''
    theta = 0.5  # ngưỡng ảnh hưởng
    c_score = 0
    q = 1  # tỷ lệ ảnh hưởng
    visited = set()
    path_prob = 1 # xác suất lan truyền
    edge_prob = {} # xác suất lan truyền qua cạnh
    c_score = dfs(visited, out_connection, path_prob, in_connection, node, theta, q, edge_prob)
    return c_score


def dfs(visited, out_connection, path_prob, in_connection, node, theta, q, edge_probs):
    if node not in visited:
        visited.add(node)
        if node in out_connection:
            for neighbour in out_connection[node]:
                path_prob *= q / in_connection[neighbour]
                edge_probs[(node, neighbour)] = path_prob  # Lưu xác suất lan truyền qua cạnh
                if path_prob >= theta:
                    dfs(visited, out_connection, path_prob, in_connection, neighbour, theta, q, edge_probs)
                    path_prob /= (q / in_connection[neighbour])
                else:
                    path_prob /= (q / in_connection[neighbour])
    N_of_nodes = len(visited)
    return N_of_nodes


def greedy(edges, n):
    ''' select seeds by greedy policy
    args:
        edges (list of list) [#edge, 2]: edge list of the graph;
        n (int): number of seeds;
    returns:
        seeds: (list) [#seed]: selected seed nodes index;
    '''
    out_degree = {}
    seeds = []
    for edge in edges:
        if edge[0] in out_degree:
            out_degree[edge[0]] += 1
        else:
            out_degree[edge[0]] = 1
    while len(seeds) < n:
        seed = sorted(out_degree.items(), key=lambda item: item[1], reverse=True)[0][0]
        seeds.append(seed)
        out_degree[seed] = -1
    return seeds


def degree(edges, n):
    ''' Select seeds by degree policy
    Args:
        edges (list of list) [#edge, 2]: edge list of the graph;
        n (int): number of seeds;
    Returns:
        seeds: (list) [#seed]: selected seed nodes index;
    '''
    degree = {}
    seeds = []
    for edge in edges:
        if edge[0] in degree:
            degree[edge[0]] += 1
        else:
            degree[edge[0]] = 1
        if edge[1] in degree:
            degree[edge[1]] += 1
        else:
            degree[edge[1]] = 1
    seeds = list({k: v for k, v in sorted(degree.items(), key=lambda item: item[1], reverse=True)}.keys())[:n]
    return seeds


def random(nodes, n):
    ''' Select seeds randomly
    Args:
        nodes (list) [#node]: node list of the graph;
        n (int): number of seeds;
    Returns:
        seeds: (list) [#seed]: selected seed nodes index;
    '''
    np.random.shuffle(nodes)
    return nodes[:n]


def degree_discount(edges, n):
    ''' Select seeds by degree discount degree
    Args:
        edges (list of list) [#edge, 2]: edge list of the graph;
        n (int): number of seeds;
    Returns:
        seeds: (list) [#seed]: selected seed nodes index;
    '''
    out_degree = {}
    connection = {}
    seeds = []
    for edge in edges:
        if edge[1] in connection:
            connection[edge[1]].append(edge[0])
        else:
            connection[edge[1]] = [edge[0]]
        if edge[0] in out_degree:
            out_degree[edge[0]] += 1
        else:
            out_degree[edge[0]] = 1
    while len(seeds) < n:
        seed = sorted(out_degree.items(), key=lambda item: item[1], reverse=True)[0][0]
        seeds.append(seed)
        out_degree[seed] = -1
        for node in connection[seed]:
            out_degree[node] -= 1
    return seeds


def degree_neighbor(edges, n):
    ''' select seeds by degree neighbor policy
    args:
        edges (list of list) [#edge, 2]: edge list of the graph;
        n (int): number of seeds;
    returns:
        seeds: (list) [#seed]: selected seed nodes index;
    '''
    out_degree = {}
    centrality_score = {}
    seeds = []
    for edge in edges:
        if edge[0] in out_degree:
            out_degree[edge[0]] += 1
        else:
            out_degree[edge[0]] = 1
    centrality_score = out_degree.copy()
    for edge in edges:
        if edge[1] in out_degree:
            centrality_score[edge[0]] += out_degree[edge[1]]
    seeds = list({k: v for k, v in sorted(centrality_score.items(), key=lambda item: item[1], reverse=True)}.keys())[:n]
    return seeds


def degree_neighbor_fix(edges, n):
    ''' select seeds by degree neighbor fix policy
    args:
        edges (list of list) [#edge, 2]: edge list of the graph;
        n (int): number of seeds;
    returns:
        seeds: (list) [#seed]: selected seed nodes index;
    '''
    out_degree = {}
    centrality_score = {}
    connection = {}
    seeds = []
    for edge in edges:
        if edge[1] in connection:
            connection[edge[1]].append(edge[0])
        else:
            connection[edge[1]] = [edge[0]]
        if edge[0] in out_degree:
            out_degree[edge[0]] += 1
        else:
            out_degree[edge[0]] = 1
    centrality_score = out_degree.copy()
    for edge in edges:
        if edge[1] in out_degree:
            centrality_score[edge[0]] += out_degree[edge[1]]
    while len(seeds) < n:
        seed = sorted(centrality_score.items(), key=lambda item: item[1], reverse=True)[0][0]
        seeds.append(seed)
        centrality_score[seed] = -1
        for node in connection[seed]:
            centrality_score[node] -= out_degree[seed]
    return seeds
