from collections import defaultdict
import random
import heapq
import utils


# format for a solution
class Individual:

    def __init__(self,
                 nodes: list,
                 edges: dict[str, dict[str, int]],
                 values: dict,
                 base_count: int,
                 genes=None):
        self.nodes = nodes
        self.edges = edges
        self.values = values
        self.base_count = base_count
        self.genes = genes
        self.fitness = 0
        self.avg_dist_to_base = None
        self.nb_without_base = None
        self.without_bases = None

        if self.genes is None:
            self.genes = set()
            # randomly initialize the genes
            while len(self.genes) < base_count:
                index = random.randint(0, len(nodes) - 1)
                self.genes.add(index)

    def copy(self):
        new = Individual(self.nodes, self.edges, self.values, self.base_count)
        new.genes = self.genes.copy()
        new.fitness = self.fitness
        new.without_bases = self.without_bases.copy()
        new.avg_dist_to_base = self.avg_dist_to_base
        new.nb_without_base = self.nb_without_base
        return new

    def update_fitness(self):
        self.fitness = 0
        self.avg_dist_to_base = 0
        self.nb_without_base = 0
        self.without_bases = []
        for node in self.nodes:
            base, base_dist = self.nearest_base_and_dist(node)
            if base is not None:
                self.fitness += base_dist * self.values[node]
                self.avg_dist_to_base += base_dist
            else:
                self.fitness += 10000
                self.nb_without_base += 1
                self.without_bases.append(node)
        self.avg_dist_to_base /= len(self.nodes)
        self.fitness = 100000 / self.fitness

    def nearest_base_and_dist(self, node):
        base = None
        base_dist = float('infinity')
        for current_base_index in self.genes:
            current_base = self.nodes[current_base_index]
            if self.edges[node][current_base] < base_dist:
                base = node
                base_dist = self.edges[node][current_base]
        return base, base_dist

    def mutation(self, probability):
        new_genes = set()
        for gene in (self.genes):
            new_gene = gene
            current_probability = probability
            for other in self.edges[gene]:
                if other in self.genes:
                    current_probability *= 5

            while random.random() < min(0.9, current_probability):
                # gene move to a random neighbour (in self.edges[gene])
                random_neighbour = random.choice(
                    list(self.edges[self.nodes[gene]].keys()))
                new_gene = self.nodes.index(random_neighbour)

                for other in self.edges[gene]:
                    if other in self.genes:
                        current_probability = 7 * probability

            new_genes.add(new_gene)
        while len(new_genes) < self.base_count:
            new_genes.add(random.randint(0, len(self.nodes) - 1))
        self.genes = new_genes

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
        s = f"fitness: {self.fitness}; nb whithout base: {self.nb_without_base}; avg dist to base: {self.avg_dist_to_base};"
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

    def call_crossover(self):
        new_individuals = [self.best_individual]
        # select two parents but more likely to select the best ones
        for _ in range(self.pop_size - 1):
            parent1 = self.select_parent()
            parent2 = self.select_parent()
            while parent1 == parent2:
                parent2 = self.select_parent()
            new_individuals.append(parent1.crossover(parent2))

    def select_parent(self):
        # select randomly an individual but more likely to select the best ones
        # sort individuals by fitness
        self.individuals.sort(key=lambda x: x.fitness, reverse=True)
        half = self.pop_size // 2
        fitness_sum = sum([ind.fitness for ind in self.individuals[:half]])
        pick = random.uniform(0, fitness_sum)
        current = 0
        for ind in self.individuals[:half]:
            current += ind.fitness
            if current > pick:
                return ind

    def mutation(self, probability):
        for individual in self.individuals:
            individual.mutation(probability)

    def next_generation(self):
        self.best_individual = None
        self.best_fitness = float('-inf')
        self.call_crossover()
        self.mutation(self.mutation_rate)
        self.call_update_fitness()
