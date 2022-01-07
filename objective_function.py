from drone import Drone
from tqdm.contrib.concurrent import process_map
from multiprocessing import cpu_count
from generation import Generation
from functools import partial
import numpy as np


def objective_function(target_list, nn):
    # create Drone associated to nn
    index = nn[1]
    nn = nn[0]
    drone = Drone(nn)
    targets_hit = 0
    drone.set_target(target_list[0])
    score = 0
    delta = 0.005
    while drone.alive:
        score += delta
        drone.update(delta)

        if np.linalg.norm(drone.target - drone.position) < 0.01:
            score += 10
            targets_hit += 1
            drone.set_target(target_list[targets_hit])

    return (nn, score, index)


def test_generation(generation, target_list):
    NNs = generation.construct_NNs()

    func = partial(objective_function, target_list)

    graded_NNs = process_map(func, NNs, max_workers=cpu_count())

    graded_NNs.sort(key=lambda x: -x[1])

    # return the indices of the best genes
    print(f"best score : {graded_NNs[0][1]}")
    generation.graded_NNs = graded_NNs
    return graded_NNs[:10]


def new_generation(generation, target_list):
    result = test_generation(generation, target_list)
    parent_indices = [x[2] for x in result]
    parents = [generation.population[index] for index in parent_indices]
    next_gen = Generation(generation.architecture, gen_num=generation.gen_num + 1)
    next_gen.construct_generation(parents)
    return next_gen
