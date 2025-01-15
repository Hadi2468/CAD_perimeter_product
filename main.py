#!/usr/bin/env python3

################################
### Perimeter Product Problem:
################################
"""
This solution consists of two steps (algorithms):
    1) Getting original edges, looking for new intersections, and making a Graph of all nodes and sub-edges.
    2) Based on available graph, look for unique sub-cycles that have no overlap with other bigger cycles. 
       Then, calculate perimeters of all unique sub-cycles, and finally calculate product of perimeters.
"""

## Import algorithms' essential functions
from make_graph import edge_intersect, create_graph
from perimeter_cycles import find_unique_cycles, calculate_perimeters
import argparse
import ast

#####################
## Input examples:
#####################
"""
edges_window_1:   Square with the size of windows in each edge 1 (simple square) (Default)            ## Output = 4.0000
edges_window_2:   Square with the size of windows in each edge 2                                      ## Output = 16.0000
edges_window_3:   Square with the size of windows in each edge 3                                      ## Output = 0.1342
edges_window_d_1: Square with the size of windows in each edge 1 plus a diameter (hourglass shape)    ## Output = 5.8284
edges_window_d_2: Square with the size of windows in each edge 2 plus a diameter in one window        ## Output = 23.3137
edges_window_d_3: Square with the size of windows in each edge 3 plus a diameter in six windows       ## Output = 0.0053
edges_test:       A complex and symmetric shape as a test of the algorithm                            ## Output = 5.5713
"""
predefined_edges = {
    'edges_window_1':   [((1, 1), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (2, 1)), ((2, 1), (1, 1))],
    'edges_window_2':   [((1, 1), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (2, 1)), ((2, 1), (1, 1)), ((1.5, 1), (1.5, 2)), ((1, 1.5), (2, 1.5))],
    'edges_window_3':   [((1, 1), (1.6, 1)), ((1, 1.2), (1.6, 1.2)), ((1, 1.4), (1.6, 1.4)), ((1, 1.6), (1.6, 1.6)), ((1, 1), (1, 1.6)), ((1.2, 1), (1.2, 1.6)), ((1.4, 1), (1.4, 1.6)), ((1.6, 1), (1.6, 1.6))], 
    'edges_window_d_1': [((1, 1), (1, 2)), ((1, 2), (2, 1)), ((2, 1), (2, 2)), ((2, 2), (1, 1))], 
    'edges_window_d_2': [((1, 1), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (2, 1)), ((2, 1), (1, 1)), ((1.5, 1), (1.5, 2)), ((1, 1.5), (2, 1.5)), ((1, 1.5), (1.5, 2))],
    'edges_window_d_3': [((1, 1), (1.6, 1)), ((1, 1.2), (1.6, 1.2)), ((1, 1.4), (1.6, 1.4)), ((1, 1.6), (1.6, 1.6)), ((1, 1), (1, 1.6)), ((1.2, 1), (1.2, 1.6)), ((1.4, 1), (1.4, 1.6)), ((1.6, 1), (1.6, 1.6)), ((1, 1.4), (1.2, 1.6)), ((1, 1.2), (1.4, 1.6)), ((1.2, 1.2), (1.6, 1.6)), ((1.4, 1.2), (1.6, 1.4))],
    'edges_test':       [((1, 1), (1, 2)), ((1, 2), (1.8, 2)), ((1.8, 2), (1.8, 1)), ((1.8, 1), (1, 1)), ((1.2, 1), (1.2, 2)), ((1.6, 1), (1.6, 2)), ((1, 1.5), (1.6, 1.8)), ((1, 1.3), (1.8, 1.7)), ((1.2, 1.2), (1.8, 1.5))]
}
###########################################################################################################################

def perimeter_product(edges):
    """
    The main function for calculating the product of all unique sub-sycles' perimeter.
    
    Input:  List (list of edges, that each edge is a tuple of start and end points)
    Output: A graph G, lists of new edges, nodes, intersections, unique cycles, and perimeter of unique cycles.
            A float number as the "Product of Perimeters"
    """ 

    iteration = 1
    last_intersection = 1
    intersections = set()
    while last_intersection != 0:
        print(f'============= Step: {iteration} =============')
        G, intersections, last_intersection = create_graph(edges, intersections, last_intersection)
        nodes = sorted(G.nodes())
        edges = list({tuple(sorted(e)) for e in G.edges()})
        last_intersection -= 1
        iteration += 1
    # print(f'New Graph Nodes: {len(nodes)}\n{nodes}')
    print(f'\nGraph Edges: {len(edges)}\n{edges}\n')
    print(f'Inntersections: {len(intersections)}\n{sorted(set(intersections))}\n')
    # print('============== >>> There are no additional interconnection!')
    
    ## Find unique cycles
    unique_cycles = find_unique_cycles(G)
    print(f'Unique Cycles: {len(unique_cycles)}\n{unique_cycles}\n')
    
    # Calculate perimeters and their product
    perimeters, product_of_perimeters = calculate_perimeters(unique_cycles)
    print(f'Perimeters of Cycles:  {perimeters}\n')
    print(f'Product of Perimeters: {product_of_perimeters:.4f}\n')

    return G, edges, intersections, unique_cycles, perimeters, product_of_perimeters


###########################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--edges', type=str, required=True, help='Edges input: 1) either a variable name of edges defined in the script (edges_window_1, edges_window_2, edges_window_3, edges_window_d_1, edges_window_d_3, edges_window_d_3, and edges_test), or 2) List of edges in the format: "[(x1,y1),(x2,y2)],[(x3,y3),(x4,y4)]"')
    args = parser.parse_args()
    edges_input = args.edges

    # Determine input format
    if edges_input.startswith('[') and edges_input.endswith(']'):
        # Parse the string representation of edges
        try:
            edges = ast.literal_eval(edges_input)
            if not isinstance(edges, list):
                raise ValueError('Input must be a list of edges.')
        except (SyntaxError, ValueError) as e:
            print(f'Invalid edges format: {e}')
            exit(1)
    else:
        # Use predefined edges by variable name
        edges = predefined_edges.get(edges_input)
        if edges is None:
            print('Error: The edges list is empty. Please provide valid edges. Here is the default edges: edges_window_1')
            edges = predefined_edges['edges_window_1']  # Default edges

    G, edges, intersections, unique_cycles, perimeters, product_of_perimeters = perimeter_product(edges)
    # print('Product of Perimeters:', product_of_perimeters)