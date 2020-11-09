Authors: Heßler, Irnich, 2020

Each instance gridW-nX-CY-VZ.gvrp is defined by
- the instance number W (W = 01, 02, ..., 90)
- the number of nodes X (X = 121, 169, 225)
- the number of clusters Y (Y = 6, 8, 10, 12, 14)
- the number of vehicles Z (Z = 2, 3, 4, 5)

For each instance we report:
NAME: instance name
COMMENT: GVRP
DIMENSION: number of nodes X
VEHICLES: number of vehicles Z
GVRP_SETS: number of clusters Y
CAPACITY: vehicle capacity
NODE_COORD_SECTION
 X lines, each indicating (for each node) node number, x-coordinate, and y-coordinate
GVRP_SET_SECTION
 Y lines, each indicating (for each cluster) cluster number and list of nodes belonging to the cluster; the end of the line is marked with -1
DEMAND_SECTION
 Y lines, each indicating (for each cluster) the demand of the cluster
EOF