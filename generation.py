import pickle
import numpy as np
from numpy.random import normal
from random import random
from nn import Network
from os import path, remove


class Generation:
    def __init__(self, architecture, gen_num=None):
        # list encoding how many neurons are in each layer
        # for example : [4,4,2] has 4 inputs, 1 hidden layer of 4 neurons and 1 output
        self.architecture = architecture
        self.gen_num = gen_num
        self.population = []
        self.nn_list = []

    @classmethod
    def first_generation(cls, architecture, mean=0, std=0.5):
        first_gen = cls(architecture, gen_num=1)
        for _ in range(100):
            gene = []
            for i in range(1, len(architecture)):
                gene += list(
                    normal(mean, std, size=architecture[i - 1] * architecture[i])
                )

                gene += list(normal(mean, std / 10, size=architecture[i]))
            first_gen.population.append(gene)
        return first_gen

    def construct_generation(self, parents, cross_over_r, mutation_r, mutation_std):
        for _ in range(50):
            offspring_1, offspring_2 = self.crossover(
                *random.sample(set(parents), 2), crossover_r
            )
            self.population.append(self.mutate(offspring_1, mutation_r, mutation_std))
            self.population.append(self.mutate(offspring_2, mutation_r, mutation_std))

    def mutate(self, offspring, mutation_r, mutation_std):
        """ basic mutation mechanism"""
        for i in range(len(offspring)):
            if random() < mutation_r:
                offspring[i] += mutation_std * normal(0, 1)

    def crossover(self, parent_1, parent_2, crossover_r):
        """
        Very basic crossover mechanism (to be improved)

        returns two offspring similar to each parent with genes exchanged at random
        """
        offspring_1, offspring_2 = [], []
        for i in range(len(parent_1)):
            if random() < crossover_r:
                offspring_1.append(parent_1[i])
                offspring_2.append(parent_2[i])
            else:
                offspring_1.append(parent_2[i])
                offspring_2.append(parent_1[i])

        return offspring_1, offspring_2

    def construct_NNs(self):
        if self.population == []:
            raise ValueError(
                "Tried to construct networks from generation with an empty population."
            )
        if self.nn_list != []:
            return self.nn_list
        nn_list = []

        for gene in self.population:
            weights = []
            biases = []
            pointer_1, pointer_2 = 0, 0
            for i in range(1, len(self.architecture)):
                pointer_2 += self.architecture[i - 1] * self.architecture[i]

                weights.append(
                    np.array(gene[pointer_1:pointer_2]).reshape(
                        (self.architecture[i - 1], self.architecture[i])
                    )
                )
                pointer_1 = pointer_2
                pointer_2 += self.architecture[i]
                biases.append(np.array(gene[pointer_1:pointer_2]))
                pointer_1 = pointer_2

            nn_list.append(Network(self.architecture, weights, biases))
        self.nn_list = nn_list
        return nn_list

    def save_generation(self):
        file_path = path.relpath(f"data/gen{self.gen_num}.pickle")
        remove(file_path)
        try:
            with open(file_path, "wb") as f:
                pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during pickling object :", ex)

    @staticmethod
    def load_generation(num):
        try:
            with open(f"data/gen{num}.pickle", "rb") as f:
                return pickle.load(f)
        except Exception as ex:
            print("Error during unpickling object :", ex)

