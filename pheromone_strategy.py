from abc import abstractmethod
import numpy as np


class PheromoneStrategy:

    @abstractmethod
    def init_pheromones(self, aco, graph):
        pass

    @abstractmethod
    def update(self, path_costs):
        pass

    @abstractmethod
    def pheromones_from(self, city):
        pass

    def start_iteration(self, t):
        pass


class BasicPheromoneStrategy(PheromoneStrategy):

    def __init__(self, Q, rho):
        self.Q = Q
        self.rho = rho

    def init_pheromones(self, aco, graph):
        self.graph = graph
        self.aco = aco
        self.indexes = list(self.graph.paths)
        self.pheromones = np.full((len(self.indexes), len(self.indexes)), 1 / len(self.indexes))

    def calculate_pheromone_delta(self, path_costs):
        deltas = np.zeros((len(self.indexes), len(self.indexes)))
        paths, costs = zip(*path_costs)

        for path, cost in zip(paths, costs):
            weighted_q = self.Q / cost

            for i in range(1, len(path)):
                prev_city = path[i-1]
                curr_city = path[i]
                deltas[prev_city, curr_city] += weighted_q

        return deltas

    def update(self, path_costs):
        pheromone_delta = self.calculate_pheromone_delta(path_costs)

        # Evaporation
        self.pheromones *= (1-self.rho)

        # Add deltas
        self.pheromones += pheromone_delta

        # Standarize pheromones
        self.pheromones = self.pheromones / self.pheromones.sum(axis=0)

    def pheromones_from(self, city):
        return self.pheromones[:, city]