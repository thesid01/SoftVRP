import sys
import pprint
import math
import CluVRP
import TSP2 as TSP
import json

class SoftCluVRPSolver:

    # Constructor
    def __init__(self):
        pass

    # Read input form file and make graph and clusters from input
    def readInput(self, fileName):
        self.fileName = fileName

        input = open(self.fileName, 'r')
        lines = input.readlines()

        self.name = lines[0].split(':')[1].strip()
        self.NumberOfNodes = int(lines[2].split(':')[1].strip())
        self.NumberOfVehicles = int(lines[3].split(':')[1].strip())
        self.NumberOfCluster = int(lines[4].split(':')[1].strip())
        self.VehicleCapacity = int(lines[5].split(':')[1].strip())
        self.NodeLocMap = dict()
        self.graph = []
        self.demands = dict()
        self.cluster = dict()

        for i in range(7, self.NumberOfNodes + 7):
            n, x, y = lines[i].split()
            self.NodeLocMap[int(n)-1] = (int(x),int(y))
        
        for i in range(self.NumberOfNodes):
            self.graph.append([0 for i in range(self.NumberOfNodes)])
        
        for i in range(self.NumberOfNodes):
            for j in range(self.NumberOfNodes):
                if i != j:
                    self.graph[i][j] = self.calculateDistance(self.NodeLocMap[i], self.NodeLocMap[j])
        
        for i in range(self.NumberOfNodes + 8, self.NumberOfNodes + 8 + self.NumberOfCluster):
            cluster = [int(c) for c in lines[i].split()]
            self.cluster[cluster[0]] = cluster[1:-1]
        
        for i in range(self.NumberOfNodes + 9 + self.NumberOfCluster, self.NumberOfNodes + 9 + 2*self.NumberOfCluster):
            demand = [int(d) for d in lines[i].split()]
            self.demands[demand[0]] = demand[1]


    # Calculate Ecludian Distance
    def calculateDistance(self, node1, node2):
        return math.sqrt( math.pow(node1[0] - node2[0], 2) + math.pow(node1[1] - node2[1], 2) )

    # Print all variables of Class
    def printAllClassVariable(self):
        with open("TXT.json", "w") as write_file:
            json.dump(vars(self), write_file)
        # print(vars(self))
        # print(pprint.pformat(vars(self), indent=4, width=1))

    # To Remove Depot
    def removeDepot(self):
        if self.graph:
            newGraph = [row[:] for row in self.graph]
            for i in range(self.NumberOfNodes):
                newGraph[0][i] = 0.0
            return newGraph
        else:
            return []

    def findCentroidsOfClusters(self):
        centroid = []
        for i in self.cluster:
            x,y = 0,0
            l = len(self.cluster[i])
            for node in self.cluster[i]:
                x = x + self.NodeLocMap[node-1][0]
                y = y + self.NodeLocMap[node-1][1]
            centroid.append([x/l,y/l])
        return centroid

    def ApplyGAonClusters(self):
        self.centroids = self.findCentroidsOfClusters()
        self.cGraph = []
        self.frontier = "---------"
        
        distances = dict()
        clusters = dict()
        trucks = ['truck' for i in range(self.NumberOfVehicles)]

        geneticProblemInstances = 20

        for i in range(self.NumberOfCluster):
            self.cGraph.append([0 for i in range(self.NumberOfCluster)])
        cap = []
        for i in range(self.NumberOfCluster):
            for j in range(self.NumberOfCluster):
                if i != j:
                    self.cGraph[i][j] = self.calculateDistance(self.centroids[i], self.centroids[j])
                else:
                    self.cGraph[i][j] = 1000
            distances[i] = self.cGraph[i][:]
            clusters[i] = "cluster "+str(i)
            cap.append((i,self.demands[i+1]))
        
        cap.append(((trucks[0],self.VehicleCapacity)))

        genetic_problem_instances = 20
        CluVRP.trucks = trucks
        CluVRP.num_trucks = len(trucks)
        CluVRP.distances = distances
        CluVRP.clusters = clusters
        CluVRP.capacity_trucks = self.VehicleCapacity
        CluVRP.frontier = self.frontier

        solution, fitness = CluVRP.VRP(genetic_problem_instances, cap)
        count = 1
        self.solutionClusters = [[]]
        print(' ')
        print('Vehicle 1: ')
        for vehicle in solution:
            if vehicle != self.frontier:
                print(vehicle)
                self.solutionClusters[-1].append(vehicle.split(' ')[1])
            else:
                print(' ')
                count = count + 1
                print('Vehicle '+str(count)+': ')
                self.solutionClusters.append([])
        return solution, fitness
    
    def ApplyTSPonClusters(self):
        self.results = []
        self.solutionClustersCustomers = []
        cities = dict()
        distances = dict()
        for clusters in self.solutionClusters:
            customers = []
            for cluster in clusters:
                for c in self.cluster[int(cluster)+1]:
                    customers.append(c)
            self.solutionClustersCustomers.append(customers)
            l = len(customers)
            tempGraph = []
            for i in range(l):
                tempGraph.append([0 for i in range(l)])
            
            for i in range(l):
                for j in range(l):
                    if i != j:
                        tempGraph[i][j] = self.calculateDistance(self.NodeLocMap[customers[i]-1], self.NodeLocMap[customers[j]-1])
                    else:
                        tempGraph[i][j] = 1000
                distances[i] = tempGraph[i][:]
                cities[i] = str(customers[i]-1)

            genetic_problem_instances = 10
            TSP.distances = distances
            TSP.cities = cities
            TSP.total_cities = l

            result = TSP.TSP(genetic_problem_instances, l)
            self.results.append(result)

        return 

# Main function
if __name__ == "__main__":
    
    dir = 'SoftCluVRPinstances/Grid/'
    fileName = 'grid02-n121-C6-V2.gvrp'

    # TODO:
        # Read file name from cmd arguments
    print('Initializing Solver')
    solver = SoftCluVRPSolver()
    print('Reading Input')
    solver.readInput(dir+fileName)
    # solver.findCentroidsOfClusters()
    print('Applying Genetic Algorithm on Cluster')
    solver.ApplyGAonClusters()
    print('Applying Genetic Algorithm on Customers')
    solver.ApplyTSPonClusters()

    solver.printAllClassVariable()