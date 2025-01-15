#!/usr/bin/env python3
###############################################
### Making a Graph of new sub-edges and nodes
###############################################

import networkx as nx


###########################################
### Looking for available intersections
###########################################
def edge_intersect(edge1, edge2, precision=6):
    """
    Looking for any available intersections between edges.
    Parameters: Two edges (list points) and a precision parameter for rounding the float numbers.
    Returns: List: list of coordination of any available intersection points
    """
    ## Coordination of two edges (start and end points)
    x1, y1 = edge1[0]
    x2, y2 = edge1[1]
    x3, y3 = edge2[0]
    x4, y4 = edge2[1]

    ## Calculate the denominator
    denom = round((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4), precision)
    if denom == 0:              # edges are parallel
        return None
    
    ## Calculate the intersection points. If needed, round them in a "precision" amount and convert them to integers.
    intersect_of_x = round(((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom, precision)
    intersect_of_y = round(((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom, precision)
    intersect_x = intersect_of_x if intersect_of_x % 1 != 0 else int(intersect_of_x)
    intersect_y = intersect_of_y if intersect_of_y % 1 != 0 else int(intersect_of_y)
    
    ## Check if the intersection points lie within the bounds of both segments
    if min(x1, x2) <= intersect_x <= max(x1, x2) and min(y1, y2) <= intersect_y <= max(y1, y2):
        if min(x3, x4) <= intersect_x <= max(x3, x4) and min(y3, y4) <= intersect_y <= max(y3, y4):
            return (intersect_x, intersect_y)
    return None


#######################
### Create a graph 
#######################
def create_graph(edges, intersections, last_intersection):
    """
    Creating a graph using Networkx library with considering of edges, and nodes (+ new intersection nodes).
    I used a parameter of "last_intersection" as a flag for the last available intersections.
    Parameters: List (list of lists of edges) and a flag parameter (last_intersection).
    Returns: a graph of G, list of new intersection points, and flag parameter (last_intersection)
    """
    ## Create a new graph using the Networkx package
    G = nx.Graph()
    # G = nx.DiGraph()
    
    ## Add the original edges to the graph using their vertices as nodes
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    # print(f'Original nodes: {len(G.nodes())}\n{G.nodes()}')
    # print(f'Original edges: {len(G.edges())}\n{G.edges()}')
    
    ## Find intersections and sub-edges
    new_edges = set()
    removal_edges = set()
    original_edges = list(G.edges())
    # print('\nIntersections based on edge indices:')
    for i in range(len(original_edges)):
        for j in range(i + 1, len(original_edges)):
            intersect = edge_intersect(original_edges[i], original_edges[j])
            ## Add new sub-edges from the intersect to the original nodes and remove original edges
            if intersect:
                n_edges = set()
                r_edges = set()
                if intersect != original_edges[i][0] and intersect != original_edges[i][1]:
                    n_edges.add((intersect, original_edges[i][0]))
                    n_edges.add((intersect, original_edges[i][1]))
                    r_edges.add((original_edges[i][0], original_edges[i][1]))
                if intersect != original_edges[j][0] and intersect != original_edges[j][1]:
                    n_edges.add((intersect, original_edges[j][0]))
                    n_edges.add((intersect, original_edges[j][1]))
                    r_edges.add((original_edges[j][0], original_edges[j][1]))
                # print(f'New sub-edges for this intersection: {len(n_edges)}\n{n_edges}')
                # print(f'Removal edges for this intersection: {len(r_edges)}\n{r_edges}')
                
                if len(n_edges) > 0:
                    for edg in n_edges:
                        new_edges.add(edg)
                if len(r_edges) > 0:
                    for edg in r_edges:
                        removal_edges.add(edg)
            
                ## Add new intersections to the nodes of graph
                if intersect not in (G.nodes()):
                    last_intersection = 3
                    intersections.add(intersect)
                    G.add_node(intersect)
    
    ## Add new edges to the graph
    # print(f'All new sub-edges: {len(new_edges)}\n{new_edges}')
    for n_edg in new_edges:
        G.add_edge(n_edg[0], n_edg[1])

    ## Remove old edges from the graph
    # print(f'All removal edges: {len(removal_edges)}\n{removal_edges}')
    for r_edg in removal_edges:
        G.remove_edge(r_edg[0], r_edg[1])

    return G, intersections, last_intersection


###########################################
if __name__ == "__main__":
    pass

