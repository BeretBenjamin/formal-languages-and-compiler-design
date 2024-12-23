class Grammar:
    def __init__(self):
        self.nonterminals = set()
        self.terminals = set()
        self.productions = {}
        self.start_symbol = None

    def read_from_file(self, filename):

        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    head, body = line.split("::=")
                    head = head.strip()
                    if self.start_symbol is None:
                        self.start_symbol = head
                    self.nonterminals.add(head)

                    productions = [prod.strip() for prod in body.split("|")]
                    if head not in self.productions:
                        self.productions[head] = []
                    self.productions[head].extend(productions)

                    for prod in productions:
                        symbols = prod.split()
                        for symbol in symbols:
                            if symbol not in self.nonterminals and not symbol.isupper():
                                self.terminals.add(symbol)

        # Existing methods...

    def compute_first(self):
        first = {symbol: set() for symbol in self.nonterminals.union(self.terminals)}

        # Terminals: FIRST of a terminal is the terminal itself
        for terminal in self.terminals:
            first[terminal].add(terminal)

        # Compute FIRST for nonterminals
        changed = True
        while changed:
            changed = False
            for head, bodies in self.productions.items():
                for body in bodies:
                    body_symbols = body.split()
                    for symbol in body_symbols:
                        old_size = len(first[head])
                        first[head].update(first[symbol] - {''})
                        if '' not in first[symbol]:
                            break
                        if old_size != len(first[head]):
                            changed = True
                    else:
                        # All symbols in the body derive epsilon
                        first[head].add('')

        return first

    def compute_follow(self):
        follow = {nonterminal: set() for nonterminal in self.nonterminals}
        follow[self.start_symbol].add('$')  # Start symbol's FOLLOW includes EOF

        first = self.compute_first()
        changed = True

        while changed:
            changed = False
            for head, bodies in self.productions.items():
                for body in bodies:
                    body_symbols = body.split()
                    for i, symbol in enumerate(body_symbols):
                        if symbol in self.nonterminals:
                            trailer = set(follow[head])
                            for next_symbol in body_symbols[i + 1:]:
                                trailer.update(first[next_symbol] - {''})
                                if '' not in first[next_symbol]:
                                    break
                            else:
                                # If we reached the end, add FOLLOW of head
                                trailer.update(follow[head])

                            old_size = len(follow[symbol])
                            follow[symbol].update(trailer)
                            if old_size != len(follow[symbol]):
                                changed = True

        return follow

    def get_nonterminals(self):
        return self.nonterminals

    def get_terminals(self):
        return self.terminals

    def get_productions(self, nonterminal):
        return self.productions.get(nonterminal, [])

    def is_cfg(self):
        # For each production, validate the left-hand side
        for head in self.productions:
            # The head must:
            # 1. Be in nonterminals
            # 2. Consist of exactly one symbol
            if head not in self.nonterminals or " " in head:
                return False
        return True

    def print_grammar(self):
        print("Nonterminals:", self.get_nonterminals())
        print("Terminals:", self.get_terminals())
        print("Productions:")
        for nonterminal in self.productions:
            print(f"  {nonterminal} ::= {' | '.join(self.productions[nonterminal])}")
        print("Is CFG:", self.is_cfg())


