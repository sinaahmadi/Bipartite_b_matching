#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
"""
    Created on Wed June 06 2018
    @author: Sina Ahmadi  (sina.ahmadi@insight-centre.org)
"""
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

try:
    import matplotlib.pyplot as plt
except:
    raise
import networkx as nx
import random
import numpy as np

import WBbM as WBbM

def plot_graph(WBbM, elarge, esmall, color):
    pos = nx.circular_layout(BG)  

    nx.draw_networkx_nodes(BG, pos,node_size=600)
    nx.draw_networkx_labels(BG, pos, font_size=15, font_family='sans-serif')
    
    nx.draw_networkx_edges(BG,pos,edgelist=elarge, width=3, edge_color=color)
    nx.draw_networkx_edges(BG,pos,edgelist=esmall, width=2, alpha=0.5, edge_color='grey', style='dashed')
    
    plt.axis('off')
    plt.show() 
    
if __name__ == "__main__":
    threshold = 9
    selected_edges = list()
    # ----------------------------------------------------------------------
    # Create a bipartite complete graph with random weights between 0 and 9.

    BG = nx.complete_bipartite_graph(10, 10)
    BG.add_weighted_edges_from((u,v,random.randint(1, 10)) for u,v in BG.edges())
    
    W = list()
            
    left, right = nx.bipartite.sets(BG)
    
    num_left, num_right = len(left), len(right)
    
    for node in left:
        node_weights = list()
        node_edges = BG.edges(node, data=True)
        for node_edge in node_edges:
            node_weights.append(node_edge[2]['weight'])
        W.append(node_weights)
 
    row_capacity, column_capacity = [1]*len(W), [1]*len(zip(*W))    
    # minimum paper cardinality
    ldp = 1
    # maximum paper cardinality with the minimum value of 2
    # can be constant or a list of all capacities. 
    udp = 2
    #udp = row_capacity
    # maximum papers one reviewer will review with the minimum value of 2
    # can be constant or a list of all capacities. 
    uda = 2
    #uda = column_capacity
    # minimum papers every reviewer has to review
    lda = 1
    # ----------------------------------------------------------------------
    # Solve the bipartite b-matching problem with the WBbM algorithm. 
    b_matching = WBbM.WBbM(num_left, num_right, [j for j in list(np.concatenate(W))] , lda, uda, ldp, udp, LogToConsole=0) 
    results, total_weight = b_matching.Bb_matching(optimization_mode = "max")

    for row_index in range(len( results )):
        for column_index in range(len( results[row_index] )):
            if results[row_index][column_index] == 1:
                selected_edges.append( (list(right)[column_index], list(left)[row_index]) ) # the order based on the gold-standard
            
    print  "Selected edges are:", selected_edges, "Total weight:", total_weight
    # ----------------------------------------------------------------------
    # Illustrate the matching output.
    elarge=[(u,v) for (u,v,d) in BG.edges(data=True) if d['weight'] > threshold]
    esmall=[(u,v) for (u,v,d) in BG.edges(data=True) if d['weight'] <= threshold]
    
    plot_graph(BG, elarge, esmall, "red") # edges with a weight over the threshold
    plot_graph(BG, selected_edges, BG.edges - selected_edges, "green") # selected edges based on the b-matching algorithm