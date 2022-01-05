from window import run_window
from drone import Drone
from objective_function import test_generation
from generation import Generation

if __name__ == "__main__":
    gen = Generation.first_generation([8, 12, 12, 2])
    # gen = Generation.load_generation(1)

    target_list = [
        (0.3, 0.4),
        (0.5, 0.8),
        (0.8, 0.4),
        (0.7, 0.1),
        (0.2, 0.5),
        (0.4, 0.9),
        (0.8, 0.1),
        (0.5, 0.5),
    ]

    best = test_generation(gen, target_list)
    print(best)

    drone = Drone(best[0][0])

    gen.save_generation()
    # drone = Drone(gen.construct_NNs()[0])
    run_window(drone=drone, target_list=target_list)

