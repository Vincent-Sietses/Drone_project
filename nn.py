import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def relu(x):
    return x * (x > 0)


class Network:
    def __init__(self, weights1, bias1, weights2, bias2, weights3, bias3):
        self.weights1 = weights1  # (dim_input, neurons1 )
        self.weights2 = weights2  # (neurons1, neurons2 )
        self.weights3 = weights3  # (neurons2, dim_output )
        self.bias1 = bias1  # (neurons1, )
        self.bias2 = bias2  # (neurons2,)
        self.bias3 = bias3  # (dim_output,)

    def forward_pass(self, input):
        layer1 = np.dot(input, self.weights1) + self.bias1
        # print(f"debug: {np.array(layer1)} \n")
        layer2 = np.dot(relu(np.array(layer1)), self.weights2) + self.bias2
        layer3 = np.dot(relu(layer2), self.weights3) + self.bias3

        return sigmoid(layer3)
