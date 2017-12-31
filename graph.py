from abc import abstractmethod
from itertools import combinations
from cached_property import cached_property

class Graph:

    @abstractmethod
    def distance(self, c1, c2):
        pass

    @abstractmethod
    def paths(self):
        pass

    @abstractmethod
    def paths_from(self, city):
        pass

    @abstractmethod
    def cities(self):
        pass

    @abstractmethod
    def cost(self, cfrom, cto):
        pass


class FullyGraph:

    def __init__(self, cost_matrix):
        self.cost_matrix = cost_matrix
        self.index = list(range(len(self.cost_matrix)))
        self.paths = list(combinations(self.index, 2))

    def distance(self, c1, c2):
        return self.cost_matrix[c1][c2]

    def paths_from(self, city):
        return [(city, other_city) for other_city in self.index if other_city != city]

    def cities(self):
        return self.index

    def cost(self, cfrom, cto):
        return self.cost_matrix[cfrom, cto]

    def __len__(self):
        return len(self.index)