from window import run_window
from drone import Drone
from objective_function import new_generation, test_generation
from generation import Generation

if __name__ == "__main__":
    # gen = Generation.first_generation([7, 14, 14, 4])
    # n = gen.construct_NNs()
    gen = Generation.load_generation(350)

    target_list = [
        (0.3, 0.3,),
        (0.3, 0.4),
        (0.4, 0.3),
        (0.5, 0.8),
        (0.8, 0.4),
        (0.7, 0.1),
        (0.2, 0.5),
        (0.4, 0.9),
        (0.8, 0.1),
        (0.5, 0.5),
    ]

    for _ in range(349):
        next_gen = new_generation(gen, target_list)
        gen.save_generation()
        gen = next_gen

    best = test_generation(gen, target_list)

    gen.save_generation()

    print(best)
    drone = Drone(best[0][0])

    run_window(drone=drone, target_list=target_list)

