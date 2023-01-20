from collections import defaultdict
import random
import heapq


# format for a solution
class Individual:
    def __init__(self, nodes, edges, values, base_count, genes=None):
        self.nodes = nodes
        self.edges = edges
        self.values = values
        self.base_count = base_count
        self.genes = genes
        self.fitness = 0

        if self.genes is None:
            self.genes = [False] * len(nodes)
            # randomly initialize the genes
            # number of True is base_count
            number_of_true = 0
            while number_of_true < base_count:
                index = random.randint(0, len(nodes) - 1)
                if not self.genes[index]:
                    self.genes[index] = True
                    number_of_true += 1

    def copy(self):
        new = Individual(self.nodes, self.edges, self.values, self.base_count)
        new.genes = self.genes.copy()
        new.fitness = self.fitness
        return new

    def update_fitness(self):
        self.fitness = 0
        nearest_bases = {}
        dist_to_base = {}
        for node in self.nodes:
            nearest_bases[node], dist_to_base[
                node] = self.get_nearest_base_and_dist(node)
        for node in dist_to_base:
            if nearest_bases[node] is not None:
                self.fitness += dist_to_base[node] * self.values[node]
            else:
                self.fitness += 30
        self.fitness = 100000 / self.fitness

    def get_nearest_base_and_dist(self, node):
        distances = self.dijkstra(node)
        nearest_base = None
        nearest_distance = float('infinity')
        for i in range(len(self.nodes)):
            node, is_base = self.nodes[i], self.genes[i]
            if is_base and distances[node] < nearest_distance:
                nearest_base = node
                nearest_distance = distances[node]
        return nearest_base, nearest_distance

    def dijkstra(self, start):
        nodes = self.nodes
        distances = defaultdict(lambda: float('infinity'))
        distances[start] = 0
        queue = [(0, start)]
        while queue:
            current_distance, current_node = heapq.heappop(queue)
            if current_distance > distances[current_node]:
                continue
            if current_node not in self.edges:
                continue
            for neighbor, weight in self.edges[current_node].items():
                distance = current_distance + weight
                if distance < 30 * 60 and distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))
        return distances

    def mutation(self, probability):
        nodes = self.nodes
        # swap two genes randomly with probability
        for _ in range(len(nodes)):
            if random.random() < probability:
                index1 = random.randint(0, len(nodes) - 1)
                index2 = random.randint(0, len(nodes) - 1)
                while index1 == index2:
                    index2 = random.randint(0, len(nodes) - 1)
                self.genes[index1], self.genes[index2] = self.genes[
                    index2], self.genes[index1]

    def crossover(self, other):
        nodes = self.nodes
        # swap two genes randomly with probability
        index = random.randint(0, len(nodes) - 1)
        new = self.copy()
        new.genes = self.genes[:index] + other.genes[index:]

        number_of_true = 0
        for gene in new.genes:
            if gene:
                number_of_true += 1

        while number_of_true != self.base_count:
            index = random.randint(0, len(nodes) - 1)
            if number_of_true > self.base_count:
                if new.genes[index]:
                    new.genes[index] = False
                    number_of_true -= 1
            else:
                if not new.genes[index]:
                    new.genes[index] = True
                    number_of_true += 1
        return new

    # Display a solution showing the maximum distance between a node and its nearest base
    # The display also shows the average distance between a node and its nearest base
    def  __str__() -> str:
        distances = []
        for node in self.nodes:
            nearest_base, dist = self.get_nearest_base_and_dist(node)
            distances.append(dist)
        return f'Fitness: {self.fitness}, Max distance: {max(distances)}, Average distance: {sum(distances) / len(distances)}'

    def get_nearest_base_and_dist() -> str :
        return ""

class Population:
    def __init__(self, pop_size, nodes, edges, values, base_count,
                 mutation_rate):
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
        self.best_fitness = -9999


    def update_fitness(self):
        for individual in self.individuals:
            individual.update_fitness()
            if individual.fitness > self.best_fitness:
                self.best_fitness = individual.fitness
                self.best_individual = individual

    def selection(self):
        # select the best half of the population
        self.individuals.sort(key=lambda x: x.fitness, reverse=True)
        self.individuals = self.individuals[:len(self.individuals) // 2]

    def crossover(self):
        # crossover the best half of the population
        for _ in range(len(self.individuals)):
            index1 = random.randint(0, len(self.individuals) - 1)
            index2 = random.randint(0, len(self.individuals) - 1)
            self.individuals.append(
                self.individuals[index1].crossover(self.individuals[index2]))

    def mutation(self, probability):
        for individual in self.individuals:
            individual.mutation(probability)

    def next_generation(self):
        self.selection()
        self.crossover()
        self.mutation(self.mutation_rate)
        self.update_fitness()


if __name__ == "__main__":
    # nodes, vertexe, values, size, base_count, genes
    nodes = ["1", "2", "3", "4", "5", "6"]
    genes = [False, False, False, False, True, False]
    vertexe = {}
    vertexe["1"] = {"2": 7, "3": 9, "6": 14}
    vertexe["2"] = {"1": 7, "3": 10, "4": 15}
    vertexe["3"] = {"1": 9, "2": 10, "4": 11, "6": 2}
    vertexe["4"] = {"2": 15, "3": 11, "5": 6}
    vertexe["5"] = {"4": 6, "6": 9}
    vertexe["6"] = {"1": 14, "3": 2, "5": 9}
    values = {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1}
    size = len(nodes)
    base_count = 1

    # create the individual
    individual = Individual(nodes, vertexe, values, base_count, genes)
    out = individual.get_nearest_base_and_dist("1")
    individual.update_fitness()
    print(individual.fitness)
