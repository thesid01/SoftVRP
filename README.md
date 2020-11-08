# SoftVRP
A repository for solving Soft VRP problem.

## Approach
1. Remove depot from cluster to get disconnected components.
2. Make a capacity cut for the components whose demand is not satisfied by a single vehicle and make cluster
3. Distribute the vehicles to each cluster.
4. Apply TSP on each cluster to get the shortest path.
5. Minimize the number of vehicles for the cluster by assigning the same vehicle to two or more cluster.
