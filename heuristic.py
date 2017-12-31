from abc import abstractmethod

class Heuristic:

    @abstractmethod
    def init_heuristic(self, aco, graph):
        pass

    @abstractmethod
    def value(self, cfrom, cities):
        pass


class DistanceHeuristic:

    def init_heuristic(self, aco, graph):
        self.graph = graph
        self.aco = aco

    def value(self, cfrom, cities):
        return 1 / self.graph.distance(cfrom, cities)