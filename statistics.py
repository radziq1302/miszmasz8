import pandas as pd
import numpy as np
from collections import Counter
import itertools
import networkx as nx


def knn(graph):
    avg_node_numbers = []
    
    for node in graph.nodes:
        neighbors = graph.adj[node].keys()
        neighbors_numbers = [len(graph.adj[neighbor_node]) for neighbor_node in neighbors]
        avg_node_numbers.append(np.mean(neighbors_numbers))
    
    avg_node_numbers = [x for x in avg_node_numbers if ~np.isnan(x)]
    
    return np.mean(avg_node_numbers)


def avg_distance(graph):
    all_nodes = graph.nodes.keys()
    all_lengths = []
    for n1, n2 in itertools.product(all_nodes, all_nodes):
        if n1 != n2:
            try:
                length = nx.shortest_path_length(graph, n1, n2)
                all_lengths.append(length)
            except nx.NetworkXNoPath:
                pass
    return np.sum(all_lengths) / (len(all_nodes)*(len(all_nodes)-1))  


def stats(graph):
    stats_dict = {}
    
    stats_dict['N'] = graph.number_of_nodes()
    print("N: " + str(stats_dict['N']))
    stats_dict['E'] = graph.number_of_edges()
    print("E: " + str(stats_dict['E']))
    stats_dict['knn'] = knn(graph)
    print("knn: " + str(stats_dict['knn']))
    stats_dict['corr'] = nx.degree_pearson_correlation_coefficient(graph)
    print("corr: " + str(stats_dict['corr']))
    stats_dict['avg_dist'] = avg_distance(graph)
    print("avg_dist: " + str(stats_dict['avg_dist']))
    
    return stats_dict