# CAD_perimeter_product
# CAD Perimeter Product
In this problem, a list of line segments is given, and each segment has the coordination of its start and end points:

[((x1, y1), (x2, y2)), ((x1, y1), (x3, y3)), ((x3, y3), (x4, y4)), …] 

I want to calculate the multiplicative product of
all perimeters of all the individual enclosed areas. To solve this problem, I used graph theory and considered each line segment as the edge of the graph, and all points as nodes of the graph. Then,
using graph modeling, find all unique sub-loops, then calculate their perimeters. 

## Repository organization
This repository has one main file, main.py, and two helper files.
\
\
**-  main.py**\
Compute perimeter product for entered line segments

```
python3 main.py [-h] -e input_edges
```

Positional argument:
- input_edges: \
  Two edges (list points) and a precision parameter for rounding the float numbers.\
  The format of input_edges: (list of edges, that each edge is a tuple of start and end points)
   - A variable name of edges defined in the script:\
       (edges_window_1, edges_window_2, edges_window_3,\
        edges_window_d_1, edges_window_d_2, edges_window_d_3,\
        edges_test)
   - A list of edges in the format:\
        "[(x1, y1), (x2, y2)], [(x3, y3), (x4, y4)], ..." 

Returns:
  1) List of all new sub-edges
  2) List of all available intersections (new nodes)
  3) List of all unique sub-cycles
  4) List of perimeters of all unique sub-cycles
  5) Product of all perimeters (float number)

\
\
![Screenshot 2025-01-14 11 38 48 PM](https://github.com/user-attachments/assets/e9ac56f3-51d2-4801-9a5d-326597ba254f)

\
\
\
**-   make_graph.py**\
Creat a graph of nodes and edges. Using 'edge-intersect()' function all available intersections between two input edges are found. Then using 'create_graph()' function, and Networkx library, all edges and new nodes (with considering new intersections) considered to creat a graph G. This algorithm is repeated until the 'last_intersection' parameter, which is considered as a flag for the last available intersections, trigged.

Input parameters:
  1) Two edges (list points)
  2) A 'precision' parameter for rounding the float numbers
  3) A flag 'last_intersection' parameter for detecting the last possible intersections in the graph

Returns:
  1) The graph of G for all sub-edges and nodes
  2) List: list of coordination of any available sub-edges
  3) List: list of coordination of any available intersection points
  4) Final flag of 'last_intersection' parameter

\
\
**-   perimeter_cycles.py**\
Compute perimeter product for entered line segments. Find all unique sub-cycles that have no overlap (80%) with other big cycles using 'find_unique_cycles()' and 'approximate_subset()' functions. Then calculate the perimeter of each cycle, the product of all perimeters, and round with the precision of 6 for float numbers using 'calculate_perimeters()' function.

Input parameters:
  1) The graph of G: graph of cycles, nodes, and edges
  2) A 'precision' parameter for rounding the float numbers
  3) A 'threshold=0.8' parameter: the accepted subset proportion based on one or two new intersections that are uncommon in other original cycles

Returns:
  1) List of unique cycles: list of cycles, where each cycle is a list of coordinates
  2) List of perimeters
  3) A product of perimeters (float number)
