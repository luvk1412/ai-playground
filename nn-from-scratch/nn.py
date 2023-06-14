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
        return res.tanh()

    def parameters(self):
        return self.w + [self.b]


class Layer(Module):

    def __init__(self, neuron_input_ct, neuron_ct):
        self.neurons = [Neuron(neuron_input_ct) for _ in range(neuron_ct)]

    def __call__(self, x):
        out = [n(x) for n in self.neurons]
        return out[0] if len(out) == 1 else out

    def parameters(self):
        return [p for neuron in self.neurons for p in neuron.parameters()]


class MLP(Module):

    def __init__(self, neuron_input_ct, layers_sz):
        all_layers_sz = [neuron_input_ct] + layers_sz
        self.layers = [Layer(all_layers_sz[i], all_layers_sz[i + 1]) for i in range(len(all_layers_sz) - 1)]

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]


if __name__ == '__main__':
    model = MLP(3, [4, 4, 1])
    xs = [
        [2.0, 3.0, -1.0],
        [3.0, -1.0, 0.5],
        [0.5, 1.0, 1.0],
        [1.0, 1.0, -1.0]
    ]
    ys = [1.0, -1.0, -1.0, 1.0]

    ypred = [model(x) for x in xs]
    loss = sum((ypredi - ysi) ** 2 for ypredi, ysi in zip(ypred, ys))
    loss.backward()
