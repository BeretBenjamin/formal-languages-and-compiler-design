from pair import Pair


class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]  # Creates a list of empty lists

    def find_by_pos(self, pos):
        if len(self.table) <= pos.first or len(self.table[pos.first]) <= pos.second:
            raise IndexError("Invalid position")

        return self.table[pos.first][pos.second]

    def get_size(self):
        return self.size

    def find_position_of_term(self, term):
        pos = self.hash(term)

        if self.table[pos]:
            for i, elem in enumerate(self.table[pos]):
                if elem == term:
                    return Pair(pos, i)

        return None

    def hash(self, key):
        sum_chars = sum(ord(c) for c in key)
        return sum_chars % self.size

    def contains_term(self, term):
        return self.find_position_of_term(term) is not None

    def add(self, term):
        """Add a term to the table and return its position"""
        if self.contains_term(term):  # If the term is already in the table, return its position
            return self.find_position_of_term(term)

        pos = self.hash(term)  # Calculate the hash to get the bucket index
        self.table[pos].append(term)  # Add the term to the corresponding bucket
        return Pair(pos, len(self.table[pos]) - 1)  # Return the position as a Pair (bucket, index in bucket)

    def __str__(self):
        return f"SymbolTable {{ elements={self.table}, size = {self.size} }}"


