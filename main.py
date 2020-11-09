import sys
import pprint
import math

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
        print(vars(self))
        # print(pprint.pformat(vars(self), indent=4, width=1))

# Main function
if __name__ == "__main__":
    dir = 'SoftCluVRPinstances/Grid/'
    fileName = 'grid01-n121-C6-V2.gvrp'

    # TODO:
        # Read file name from cmd arguments

    solver = SoftCluVRPSolver()
    solver.readInput(dir+fileName)
    
    # solver.printAllClassVariable()