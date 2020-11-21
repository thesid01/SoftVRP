import random
from random import randrange
from time import time 


class Problem_Genetic(object): 
    def __init__(self,genes,individuals_length,decode,fitness):
        self.genes= genes
        self.individuals_length= individuals_length
        self.decode= decode
        self.fitness= fitness


    def mutation(self, chromosome, prob):
            
            def inversion_mutation(chromosome_aux):
                chromosome = chromosome_aux
                index1 = randrange(0,len(chromosome))
                index2 = randrange(index1,len(chromosome))
                chromosome_mid = chromosome[index1:index2]
                chromosome_mid.reverse()
                chromosome_result = chromosome[0:index1] + chromosome_mid + chromosome[index2:]
                
                return chromosome_result
        
            aux = []
            for _ in range(len(chromosome)):
                if random.random() < prob :
                    aux = inversion_mutation(chromosome)
            return aux

    def crossover(self,parent1, parent2):

        def process_gen_repeated(copy_child1,copy_child2):
            count1=0
            for gen1 in copy_child1[:pos]:
                repeat = 0
                repeat = copy_child1.count(gen1)
                if repeat > 1:#If need to fix repeated gen
                    count2=0
                    for gen2 in parent1[pos:]:#Choose next available gen
                        if gen2 not in copy_child1:
                            child1[count1] = parent1[pos:][count2]
                        count2+=1
                count1+=1

            count1=0
            for gen1 in copy_child2[:pos]:
                repeat = 0
                repeat = copy_child2.count(gen1)
                if repeat > 1:#If need to fix repeated gen
                    count2=0
                    for gen2 in parent2[pos:]:#Choose next available gen
                        if gen2 not in copy_child2:
                            child2[count1] = parent2[pos:][count2]
                        count2+=1
                count1+=1

            return [child1,child2]

        pos=random.randrange(1,self.individuals_length-1)
        child1 = parent1[:pos] + parent2[pos:] 
        child2 = parent2[:pos] + parent1[pos:] 
        
        return  process_gen_repeated(child1, child2)
        

def decodeTSP(chromosome):    
    lista=[]
    for i in chromosome:
        lista.append(cities.get(i))
    return lista


def penalty(chromosome):
        actual = chromosome
        value_penalty = 0
        for i in actual:
            times = 0
            times = actual.count(i) 
            if times > 1:
                value_penalty+= 100 * abs(times - len(actual))
        return value_penalty


def fitnessTSP(chromosome):
    
    def distanceTrip(index,city):
        w = distances.get(index)
        return  w[city]
        
    actualChromosome = list(chromosome)
    fitness_value = 0
    count = 0
    
    # Penalty for a city repetition inside the chromosome
    penalty_value = penalty(actualChromosome)
 
    for i in chromosome:
        if count==total_cities - 1:
            nextCity = actualChromosome[0]
        else:    
            temp = count+1
            nextCity = actualChromosome[temp]
         
        fitness_value+= distanceTrip(i,nextCity) + 50 * penalty_value
        count+=1
        
    return fitness_value

def genetic_algorithm_t(Problem_Genetic,k,opt,ngen,size,ratio_cross,prob_mutate):
    
    def initial_population(Problem_Genetic,size):   
        def generate_chromosome():
            chromosome=[]
            for i in Problem_Genetic.genes:
                chromosome.append(i)
            random.shuffle(chromosome)
            return chromosome
        return [generate_chromosome() for _ in range(size)]
            
    def new_generation_t(Problem_Genetic,k,opt,population,n_parents,n_directs,prob_mutate):
        
        def tournament_selection(Problem_Genetic,population,n,k,opt):
            winners=[]

            for _ in range(int(n)):
                elements = random.sample(population,k)
                winners.append(opt(elements,key=Problem_Genetic.fitness))
            return winners
        
        def cross_parents(Problem_Genetic,parents):
            childs=[]
            for i in range(0,len(parents),2):
                childs.extend(Problem_Genetic.crossover(parents[i],parents[i+1]))
            return childs
    
        def mutate(Problem_Genetic,population,prob):
            for i in population:
                Problem_Genetic.mutation(i,prob)
            return population
                        
        directs = tournament_selection(Problem_Genetic, population, n_directs, k, opt)
        crosses = cross_parents(Problem_Genetic,
                                tournament_selection(Problem_Genetic, population, n_parents, k, opt))
        mutations = mutate(Problem_Genetic, crosses, prob_mutate)
        new_generation = directs + mutations
        
        return new_generation
    
    population = initial_population(Problem_Genetic, size)
    n_parents= round(size*ratio_cross)
    n_parents = (n_parents if n_parents%2==0 else n_parents-1)
    n_directs = int(size - n_parents)
    
    for _ in range(ngen):
        population = new_generation_t(Problem_Genetic, k, opt, population, n_parents, n_directs, prob_mutate)
    
    bestChromosome = opt(population, key = Problem_Genetic.fitness)
    # print("Chromosome: ", bestChromosome)
    genotype = Problem_Genetic.decode(bestChromosome)
    # print ("Solution:" , (genotype,Problem_Genetic.fitness(bestChromosome)))
    return (genotype,Problem_Genetic.fitness(bestChromosome))

def TSP(k,n):
    dummy = [i for i in range(n)]
    TSP_PROBLEM = Problem_Genetic(dummy,n, lambda x : decodeTSP(x), lambda y: fitnessTSP(y))
    
    def first_part_GA(k):
        cont  = 0
        print('Please Wait...')
        tiempo_inicial_t2 = time()
        minfitness = None
        bestSolution = None

        while cont <= k: 
            genotype, fitness = genetic_algorithm_t(TSP_PROBLEM, 2, min, 200, 100, 0.8, 0.05)
            if minfitness:
                if minfitness > fitness:
                    minfitness = fitness
                    bestSolution = genotype
            else:
                minfitness = fitness
                bestSolution = genotype

            cont+=1
        tiempo_final_t2 = time() 
        print("")
        print("Total time: ",(tiempo_final_t2 - tiempo_inicial_t2)," secs.\n")
        return (bestSolution, minfitness)
     
    
    solution = first_part_GA(k)
    return solution
    print("------------------------------------------------------------------------------------------------------------------------------------------------------------------")
#---------------------------------------- AUXILIARY DATA FOR TESTING --------------------------------


# cities = {0:'Almeria',1:'Cadiz',2:'Cordoba',3:'Granada',4:'Huelva',5:'Jaen',6:'Malaga',7:'Sevilla'}

#Distance between each pair of cities

# w0=[999,454,317,165,528,222,223,410]
# w1=[453,999,253,291,210,325,234,121]
# w2=[317,252,999,202,226,108,158,140]
# w3=[165,292,201,999,344,94,124,248]
# w4=[508,210,235,346,999,336,303,94]
# w5=[222,325,116,93,340,999,182,247]
# w6=[223,235,158,125,302,185,999,206]
# w7=[410,121,141,248,93,242,199,999]

# distances = {0:w0,1:w1,2:w2,3:w3,4:w4,5:w5,6:w6,7:w7}
# total_cities


if __name__ == "__main__":

    # Constant that is an instance object 
    genetic_problem_instances = 10
    print("EXECUTING ", genetic_problem_instances, " INSTANCES \n")
    TSP(genetic_problem_instances)
