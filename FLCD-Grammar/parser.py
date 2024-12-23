class RecursiveDescentParser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.input = []
        self.index = 0
        self.stack = []

    def parse(self, input_string):
        self.input = input_string.split() + ['$']
        self.index = 0
        self.stack = [self.grammar.start_symbol]

        while self.stack:
            top = self.stack.pop()
            current_input = self.input[self.index]

            if top in self.grammar.terminals or top == '$':
                if top == current_input:
                    self.advance()
                else:
                    self.momentary_insuccess()
            elif top in self.grammar.nonterminals:
                self.expand(top, current_input)
            else:
                raise Exception("Unexpected symbol in stack")

        if self.index == len(self.input) - 1:
            self.success()
        else:
            self.momentary_insuccess()

    def expand(self, nonterminal, current_input):
        for production in self.grammar.get_productions(nonterminal):
            first_set = self.grammar.compute_first()[production.split()[0]]
            if current_input in first_set or ('' in first_set and current_input in self.grammar.compute_follow()[nonterminal]):
                self.stack.extend(reversed(production.split()))
                return
        self.momentary_insuccess()

    def advance(self):
        self.index += 1

    def momentary_insuccess(self):
        raise Exception("Parsing failed")

    def success(self):
        print("Parsing succeeded")
