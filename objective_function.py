from drone import Drone
from tqdm.contrib.concurrent import process_map
from multiprocessing import cpu_count
from generation import Generation
from functools import partial
import numpy as np


def objective_function(target_list, nn):
    # create Drone associated to nn
    drone = Drone(nn)
    targets_hit = 0
    drone.set_target(target_list[0])
    score = 0
    delta = 0.005
    while drone.alive:
        score += 0.1 * delta
        drone.update(delta)

        if np.linalg.norm(drone.target - drone.position) < 0.01:
            score += 10
            targets_hit += 1
            drone.set_target(target_list[targets_hit])

    return (nn, score)


def test_generation(generation, target_list):
    NNs = generation.construct_NNs()

    func = partial(objective_function, target_list)

    graded_NNs = process_map(func, NNs, max_workers=cpu_count())

    graded_NNs.sort(key=lambda x: -x[1])

    return graded_NNs[:10]

