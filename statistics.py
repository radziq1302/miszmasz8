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


def wspolczynnik_gronowania(graph):
    
    c_i_list = []
    
    for node in list(graph.nodes):
        neighbors = graph.adj[node].keys()
        node_neighbor_egdes = 0
        for n1, n2 in itertools.product(neighbors, neighbors):
            if n1 != n2 and graph.has_edge(n1, n2):
                node_neighbor_egdes += 1
 
        node_all_possible_egdes = graph.degree[node] * (graph.degree[node]-1)/2
        
        if node_all_possible_egdes != 0:
            c_i = node_neighbor_egdes / node_all_possible_egdes
            c_i_list.append(c_i)
        else:
            return None
    
    return np.mean(c_i_list)


def stats(graph):
    stats_dict = {}
    
    stats_dict['N'] = graph.number_of_nodes()
    print("Liczba węzłów: " + str(stats_dict['N']))
    stats_dict['E'] = graph.number_of_edges()
    print("Liczba krawędzi: " + str(stats_dict['E']))
    stats_dict['knn'] = knn(graph)
    print("Średni stopień najbliższego węzła: " + str(stats_dict['knn']))
    stats_dict['corr'] = nx.degree_pearson_correlation_coefficient(graph)
    print("Współczynnik korelacji: " + str(stats_dict['corr']))
    stats_dict['wsp_gron'] = wspolczynnik_gronowania(graph)
    print("Współczynnik gronowania: " + str(stats_dict['wsp_gron']))
    
    # zdecydowaliśmy się na wykorzystanie funkcji z biblioteki nx, ponieważ działa zdecydowanie szybciej
    stats_dict['avg_dist'] = nx.average_shortest_path_length(graph)
    print("Średni dystans: " + str(stats_dict['avg_dist']))
   
    