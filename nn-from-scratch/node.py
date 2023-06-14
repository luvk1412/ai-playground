import math
from draw import draw_dot


def _get_or_create_node(other):
    other = other if isinstance(other, Node) else Node(other)
    return other


class Node:

    def __init__(self, data, _children=(), _op=''):
        self.data = data
        self.grad = 0

        self._backward = lambda: None
        self._prev = _children
        self._op = _op

    def __repr__(self) -> str:
        return f"Value(data={self.data}, grad={self.grad})"

    def __add__(self, other):
        other = _get_or_create_node(other)
        res = Node(self.data + other.data, (self, other), '+')

        def _backward():
            self.grad += res.grad
            other.grad += res.grad

        res._backward = _backward
        return res

    def __mul__(self, other):
        other = _get_or_create_node(other)
        res = Node(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * res.grad
            other.grad += other.data * res.grad

        res._backward = _backward
        return res

    def __pow__(self, power):
        assert isinstance(power, (int, float)), "power needs to be int or float"
        res = Node(self.data ** power, (self,), f'**{power}')

        def _backward():
            self.grad += power * (self.data ** (power - 1)) * res.grad

        res._backward = _backward
        return res

    def tanh(self):
        res = Node(math.tanh(self.data), (self,), "tanh")

        def _backward():
            self.grad = (1 - (res.data ** 2)) * res.grad

        res._backward = _backward
        return res

    def __neg__(self):
        return self * -1

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self * (other ** -1)

    def __rtruediv__(self, other):
        return other * (self ** -1)

    def backward(self):

        # topological order all the children in the graph
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)

        # go one variable at a time and apply the chain rule to get its gradient
        self.grad = 1
        for v in reversed(topo):
            v._backward()


if __name__ == '__main__':
    n1 = Node(2)
    n2 = Node(4)
    n3 = n1 * n2
    n3.tanh()
    n3.backward()
    print(n3._prev)
    draw_dot(n3)
    print("Done")
