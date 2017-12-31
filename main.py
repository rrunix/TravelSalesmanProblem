import ACO
import select_strategy
import heuristic as h
import pheromone_strategy
from graph import FullyGraph
import plot
import matplotlib.pyplot as plt

import numpy as np
from scipy.spatial import distance


def graph_from(file):
    points = []
    with open(file, 'r') as f:
        for line in f.readlines():
            city = line.split(' ')
            points.append((int(city[1]), int(city[2])))

    size = len(points)
    cost_matrix = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            cost_matrix[i, j] = distance.euclidean(points[i], points[j])

    return points, FullyGraph(cost_matrix)


points, graph = graph_from("data/chn144.txt")
n_ants = 10
iterations = 100
alpha = 3
beta = 1
q = 10
rho = 0.01

heuristic = h.DistanceHeuristic()
select = select_strategy.BaseSelectStrategy(alpha, beta, heuristic)
pheromone = pheromone_strategy.BasicPheromoneStrategy(q, rho)


aco = ACO.ACO(n_ants, select, pheromone)
res = aco.solve(iterations, graph, 1)

best = res[0]
plot.plot(points, best[0])
print(best[1])
