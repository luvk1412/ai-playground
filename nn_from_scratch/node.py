def _get_or_create_node(other):
    other = other if isinstance(other, Node) else Node(other)
    return other


class Node:
    """ stores a single scalar value and its gradient """

    def __init__(self, data, _children=(), _op=''):
        self.data = data
        self.grad = 0
        self._prev = _children
        self._op = _op

    def __repr__(self) -> str:
        return f"Value(data={self.data}, grad={self.grad})"

    def __add__(self, other):
        other = _get_or_create_node(other)
        res = Node(self.data + other.data, (self, other), '+')
        return res

    def __mul__(self, other):
        other = _get_or_create_node(other)
        res = Node(self.data * other.data, (self, other), '*')
        return res

    def __pow__(self, power):
        assert isinstance(power, (int, float)), "power needs to be int or float"
        res = Node(self.data ** power, (self, power), f'**{power}')
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


if __name__ == '__main__':
    n1 = Node(2)
    n2 = Node(4)

    print(n1 + n2)
    print(n1 * n2)
    print(16 / n2)
    print(n1**3)
