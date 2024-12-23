class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return f"Pair{{first={self.first}, second={self.second}}}"

    def __repr__(self):
        return f"Pair({self.first}, {self.second})"

    def __eq__(self, other):
        if isinstance(other, Pair):
            return self.first == other.first and self.second == other.second
        return False

    def __hash__(self):
        return hash((self.first, self.second))