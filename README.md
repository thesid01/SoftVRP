# SoftVRP
A repository for solving Soft VRP problem.

## Approach
1. Take Input -  https://logistik.bwl.uni-mainz.de/files/2020/01/SoftCluVRPinstances.zip
2. Remove depot from cluster to get disconnected components.
3. Do preprocessing on each cluster - https://sci-hub.se/https://doi.org/10.1287/trsc.1100.0352
2. Make a capacity cut on each cluster.
3. Distribute the vehicles to each cluster.
4. Apply GA on each cluster.
5. Minimize the number of vehicles for the cluster by assigning the same vehicle to two or more cluster.

## Input Format
```bash
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
```