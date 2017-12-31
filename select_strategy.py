from abc import abstractmethod
import numpy as np


class SelectStrategy:

    def init_selection_strategy(self, aco, graph):
        pass

    @abstractmethod
    def next(self, ant):
        pass

    @abstractmethod
    def initial_city(self, ant):
        pass

    def start_iteration(self, t):
        pass


class RandomSelectStrategy:

    def init_selection_strategy(self, aco, graph):
        self.graph = graph

    @abstractmethod
    def next(self, ant):
        available = list(set(self.graph.cities()) - set(ant.path))
        return ant.rand.choice(available)


    @abstractmethod
    def initial_city(self, ant):
        return ant.rand.choice(self.graph.cities())


class BaseSelectStrategy(SelectStrategy):

    def __init__(self, alpha, beta, heuristic):
        self.alpha = alpha
        self.beta = beta
        self.heuristic = heuristic

    def init_selection_strategy(self, aco, graph):
        self.graph = graph
        self.aco = aco
        self.pheromone_strategy = self.aco.pheromone_strategy
        self.heuristic.init_heuristic(aco, graph)

    def next(self, ant):
        available = list(set(self.graph.cities()) - set(ant.path))

        pheromones = self.pheromone_strategy.pheromones_from(ant.prev_city)[available]

        # Probability of choosing the next city
        next_city_prob = np.power(pheromones, self.alpha) * \
                         np.power(self.heuristic.value(ant.prev_city, available), self.beta)
        next_city_prob = next_city_prob / next_city_prob.sum(axis=0)

        return np.random.choice(available, p=next_city_prob)

    def initial_city(self, ant):
        return ant.rand.choice(self.graph.cities())
