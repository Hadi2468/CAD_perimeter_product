#!/usr/bin/env python3
#####################################################################################################
### Finding unique cycles and calculating their perimeters, and finally calculate product of them
#####################################################################################################

import networkx as nx
import math


#################################
### Finding unique cycles
#################################
def approximate_subset(list1, list2, threshold=0.8):
    """
    Look for an approximate subset of two cycles while considering a threshold.
    Parameters: cycles (list of lists): List of cycles, where each cycle is a list of coordinates.
                threshold: the subset proportion we accept based on one or two new intersections that are uncommon in other original cycles.
    Returns: 1) result (Boolean) and 2) proportion (Percentage of subset)
    """
    ## Look for subset
    count = 0
    temp_list2 = list2.copy()        # To ensure duplicates are handled correctly
    for item in list1:
        if item in temp_list2:
            count += 1
            temp_list2.remove(item)  # Remove one occurrence of the item
    
    ## Calculate the proportion
    proportion = count / len(list1)
    return proportion >= threshold, proportion


def find_unique_cycles(G):
    """
    Find all unique sub-cycles that have no overlap (85%) with other big cycles.
    Parameters: graph (G): graph of cycles, nodes, and edges.
    Returns: cycles (list of unique cycles)
    """
    ## Find simple cycles (all available cycles) of graph G
    all_cycles = list(nx.simple_cycles(G))
    sub_cycles = sorted(all_cycles, key=len, reverse=True)    # Sort by size, largest first
    # print('sub_cycles:\n', len(sub_cycles))
    remove_cycles = []        # list of overlapped big cycles that should be removed to keep only unique sub-cycles
    len_cycles = 1000         # a parameter for repeating while loop based on maximum possible intersections in one edge
    stop_flag = 0
    while len_cycles != stop_flag:
        for i in sub_cycles:
            # print('i:========= ', i)
            stop_flag = len(sub_cycles)
            for j in sub_cycles:
                if j not in remove_cycles:
                    # print('j:', j)
                    result, proportion = approximate_subset(j, i)
                    if (result or set(j).issubset(set(i))) and i != j:
                        remove_cycles.append(i)
                        # print(f'removed cycles: {len(remove_cycles)}\n{remove_cycles}')
                        # print(f'new_sub_cycles: {len(sub_cycles)}\n{sub_cycles}')
                        break
        # print(f'\nsub_cycles: {len(sub_cycles)}\n{sub_cycles}')
        # print(f'\nremove_cycles: {len(remove_cycles)}\n{}')
        sub_cycles = [s for s in sub_cycles if s not in remove_cycles]
        # print(f'\nsub_cycles: {len(sub_cycles)}\n{sub_cycles}')
        # print('stop_flag: ', stop_flag)
        len_cycles = len(sub_cycles)
        unique_cycles = sub_cycles
        # print(f'\nunique_cycles: {len(unique_cycles)}\n{unique_cycles}')
    return unique_cycles



    # Convert undirected graph to directed graph
    directed_G = G.to_directed()

    # Use simple_cycles on the directed graph
    all_cycles = list(nx.simple_cycles(directed_G))
    sub_cycles = sorted(all_cycles, key=len, reverse=True)  # Sort by size, largest first

    # Find unique cycles
    remove_cycles = []
    len_cycles = 1000  # A parameter for repeating while loop
    stop_flag = 0
    while len_cycles != stop_flag:
        for i in sub_cycles:
            stop_flag = len(sub_cycles)
            for j in sub_cycles:
                if j not in remove_cycles:
                    result, proportion = approximate_subset(j, i)
                    if (result or set(j).issubset(set(i))) and i != j:
                        remove_cycles.append(i)
                        break
        sub_cycles = [s for s in sub_cycles if s not in remove_cycles]

    unique_cycles = sub_cycles
    return unique_cycles

#################################
### Calculate Perimeters
#################################
def calculate_perimeters(cycles, precision=6):
    """
    Calculate the perimeter of each cycle and the product of all perimeters. 
    Rounding with the precision of 6 for float numbers.
    Parameters: cycles (list of lists): List of cycles, where each cycle is a list of coordinates.
    Returns: tuple (list of perimeters, product of perimeters)
    """
    perimeters = []
    for cycle in cycles:
        perimeter = 0
        for i in range(len(cycle)):
            point_1 = cycle[i]
            point_2 = cycle[(i + 1) % len(cycle)]
            perimeter += round(math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2), precision)
        perimeters.append(round(perimeter, precision))
    
    ## Calculate the product of all perimeters
    product_of_perimeters = round(math.prod(perimeters), precision)
    
    return perimeters, product_of_perimeters


###########################################
if __name__ == "__main__":
    pass