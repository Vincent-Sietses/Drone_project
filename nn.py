import numpy as np


def sigmoid(x):
    # print("sigmoid")
    # print(x)
    # print(1 / (1 + np.exp(-x)))
    return 1 / (1 + np.exp(-x))


def relu(x):
    # print("x")
    # print(x)
    # print("relu")
    # print(x * (x > 0))
    return x * (x > 0)


class Network:
    """Class for networks. TO DO : make the number of layers and neurons modular."""

    def __init__(self, architecture, weights, biases):
        self.architecture = architecture
        self.weights = weights
        self.biases = biases

    def forward_pass(self, input):
        layers = [input]

        for i in range(len(self.biases)):
            # print(layers)
            layers.append(relu(np.dot(layers[i], self.weights[i]) + self.biases[i]))
        # print(layers)
        return sigmoid(layers[-1])
