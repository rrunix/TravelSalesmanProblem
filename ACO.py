from random import Random


class Ant:

    def __init__(self, graph, select_strategy, pheromone_strategy, seed):
        self.graph = graph
        self.select_strategy = select_strategy
        self.pheromone_strategy = pheromone_strategy
        self.path = []
        self.rand = Random(seed)
        self.prev_city = None

    def reset(self):
        self.path.clear()

    def walk(self):
        self.reset()
        cost = 0

        self.prev_city = self.select_strategy.initial_city(self)
        self.path.append(self.prev_city)

        for _ in range(len(self.graph)-1):
            next_city = self.select_strategy.next(self)

            self.path.append(next_city)

            cost += self.graph.distance(self.prev_city, next_city)
            self.prev_city = next_city

        return self.path, cost


class ACO:
    def __init__(self, ant_count, select_strategy, pheromone_strategy):
        self.ant_count = ant_count
        self.select_strategy = select_strategy
        self.pheromone_strategy = pheromone_strategy

    def ant_walk(self, ant):
        return ant.walk()

    def solve(self, iterations, graph, k=None, seed=0):
        self.pheromone_strategy.init_pheromones(self, graph)
        self.select_strategy.init_selection_strategy(self, graph)

        ants = [Ant(graph, self.select_strategy, self.pheromone_strategy, seed + i) for i in range(self.ant_count)]

        bests = []

        for iteration in range(1, iterations+1):

            # Random walks by ants (Path, cost)
            path_cost = []
            for ant in ants:
                path_cost.append(ant.walk())

            # Keep k bests
            bests = sorted(bests + path_cost, key=lambda x: x[1])[:k]

            # Update pheromones
            self.pheromone_strategy.update(path_cost)

        return bests

    def solve_clustered(self, iterations, graph, k=None, seed=0):
        pass