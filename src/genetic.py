from collections import defaultdict
import random
import heapq
import utils


# format for a solution
class Individual:

    def __init__(self, nodes, edges, values, base_count, genes=None):
        self.nodes = nodes
        self.edges = edges
        self.values = values
        self.base_count = base_count
        self.genes = genes
        self.fitness = 0
        self.max_dist_to_base = None
        self.avg_dist_to_base = None
        self.max_node_to_base = None
        self.nb_without_base = None

        if self.genes is None:
            self.genes = set()
            # randomly initialize the genes
            while len(self.genes) == base_count:
                index = random.randint(0, len(nodes) - 1)
                self.genes.add(index)

    def copy(self):
        new = Individual(self.nodes, self.edges, self.values, self.base_count)
        new.genes = self.genes.copy()
        new.fitness = self.fitness
        return new

    def update_fitness(self):
        self.fitness = 0
        for node in self.nodes:
            base, base_dist = self.nearest_base_and_dist(node)
            if base is not None:
                self.fitness += base_dist * self.values[node]
                self.avg_dist_to_base += base_dist
            else:
                self.fitness += float('infinity')
                if self.nb_without_base is None:
                    self.nb_without_base = 0
                self.nb_without_base += 1
        if self.avg_dist_to_base is not None:
            self.avg_dist_to_base /= len(self.nodes)
        self.fitness = 100000 / self.fitness

    def nearest_base_and_dist(self, node):
        base = None
        base_dist = float('infinity')
        for current_base in self.genes:
            if self.edges[node][current_base] < base_dist:
                base = node
                base_dist = self.edges[node][current_base]

        if base and (self.max_dist_to_base is None
                     or base_dist > self.max_dist_to_base):
            self.max_dist_to_base = base_dist
            self.max_node_to_base = (node, base)
        return base, base_dist

    def mutation(self, probability):
        new_genes = self.genes.copy()
        for gene in range(len(self.genes)):
            while random.random() < probability:
                if random.random() < 0.5:
                    if gene != 0:
                        gene -= 1
                else:
                    if gene != len(self.genes) - 1:
                        gene += 1
            new_genes.add(gene)

    def crossover(self, other):
        new = self.copy()
        new.genes = self.genes.copy()
        index = random.randint(0, len(self.nodes) - 1)

        genes1_list = list(self.genes)
        genes2_list = list(other.genes)
        new_genes_list = genes1_list[:index] + genes2_list[index:]
        new.genes = set(new_genes_list)

        while len(new.genes) != self.base_count:
            index = random.randint(0, len(self.nodes) - 1)
            new.genes.add(index)

        return new

    # Display a solution showing the maximum distance between a node and its nearest base
    # The display also shows the average distance between a node and its nearest base
    def __str__(self) -> str:
        s = f"fitness: {self.fitness};"
        if self.max_node_to_base is None or self.avg_dist_to_base is None or self.nb_without_base is None:
            if self.max_node_to_base is None:
                s += "missing max_node_to_base;" 
            if self.avg_dist_to_base is None:
                s += "missing avg_dist_to_base;"
            if self.nb_without_base is None:
                s += "missing nb_without_base;"
            return s
        
        max_node, max_base = self.max_node_to_base

        s += "La ville la moin bien desservie est: " + str(
            max_node) + " en " + str(max_base) + "min"
        s += "La distance moyenne entre un noeud et sa base la plus proche est: " + str(
            self.avg_dist_to_base) + "\n"
        s += "Il y a " + str(
            self.nb_without_base) + " villes qui ne sont pas desservies"
        return s

    # def get_nearest_base_and_dist() -> str:
    #     return ""


class Population:

    def __init__(self, pop_size, nodes, edges, values, base_count,
                 mutation_rate):
        if len(nodes) < base_count:
            raise Exception(
                "The number of bases must be less than the number of nodes")
        self.pop_size = pop_size
        self.nodes = nodes
        self.edges = edges
        self.values = values
        self.mutation_rate = mutation_rate
        self.base_count = base_count
        self.individuals = [
            Individual(nodes, edges, values, base_count)
            for _ in range(pop_size)
        ]
        self.best_individual = None
        self.best_fitness = float('-inf')

    def call_update_fitness(self):
        for individual in self.individuals:
            individual.update_fitness()
            if individual.fitness > self.best_fitness:
                self.best_fitness = individual.fitness
                self.best_individual = individual

    def selection(self):
        # select the best half of the population
        self.individuals.sort(key=lambda x: x.fitness, reverse=True)
        self.individuals = self.individuals[:len(self.individuals) // 2]

    def call_crossover(self):
        # crossover the best half of the population
        for _ in range(len(self.individuals)):
            index1 = random.randint(0, len(self.individuals) - 1)
            index2 = random.randint(0, len(self.individuals) - 1)
            self.individuals.append(self.individuals[index1].crossover(
                self.individuals[index2]))

    def mutation(self, probability):
        for individual in self.individuals:
            individual.mutation(probability)

    def next_generation(self):
        self.best_individual = None
        self.best_fitness = float('-inf')
        self.selection()
        self.call_crossover()
        self.mutation(self.mutation_rate)
        self.call_update_fitness()
