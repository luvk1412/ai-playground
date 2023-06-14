import random

from node import Node


class Module:

    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0

    def parameters(self):
        return []


class Neuron(Module):

    def __init__(self, neuron_input_ct):
        self.w = [Node(random.uniform(-1, 1)) for _ in range(neuron_input_ct)]
        self.b = Node(random.uniform(0, 1))

    def __call__(self, x):
        res = sum((wi * xi for wi, xi in zip(self.w, x)), self.b)
        return res

    def parameters(self):
        return self.w + [self.b]


class Layer(Module):

    def __init__(self, neuron_input_ct, neuron_ct):
        self.neurons = [Neuron(neuron_input_ct) for _ in range(neuron_ct)]

    def parameters(self):
        return super().parameters()
