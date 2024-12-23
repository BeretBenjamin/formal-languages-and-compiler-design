import re
from symbol_table import SymbolTable
from pair import Pair

class LexicalAnalyzer:
    def __init__(self, token_file):
        self.tokens = {}
        self.symbol_table = SymbolTable(100)
        self.pif = []
        self.load_tokens(token_file)

    def load_tokens(self, token_file):
        """Load keywords and operators from the token file."""
        with open(token_file, "r") as file:
            for idx, line in enumerate(file, start=1):
                parts = line.strip().split()
                if len(parts) == 1:
                    self.tokens[parts[0].upper()] = idx  # e.g., 'PROGRAM' -> 1
                else:
                    self.tokens[parts[1].upper()] = idx  # e.g., ':=' -> 13

    def is_identifier(self, token):
        """Check if a token is a valid identifier."""
        return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token) is not None

    def is_integer_constant(self, token):
        """Check if a token is a valid integer constant."""
        return re.match(r'^[+-]?[0-9]+$', token) is not None

    def analyze(self, program_file):
        """Analyze the program line by line."""
        # Patterns for tokens
        token_pattern = re.compile(
            r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'  # Identifiers
            r'|[+-]?\b\d+\b'               # Integer constants
            r'|>=|<=|:=|!=|==|[;:()\[\]{}]'  # Multi-char and single-char tokens
            r'|[^ \t\n]'                   # Catch-all for unrecognized tokens
        )

        with open(program_file, "r") as file:
            for line_num, line in enumerate(file, start=1):
                tokens = re.findall(token_pattern, line.strip())  # Tokenize the line

                for token in tokens:
                    token_upper = token.upper()  # Handle case-insensitive keywords and operators

                    # Check if the token is a keyword or operator
                    if token_upper in self.tokens:
                        self.pif.append((token, self.tokens[token_upper]))

                    # Check if the token is an identifier
                    elif self.is_identifier(token):
                        if not self.symbol_table.contains_term(token):
                            pos = self.symbol_table.add(token)
                            print(f"'{token}' added to Symbol Table at position {pos}.")
                        else:
                            print(f"'{token}' is already in the Symbol Table.")
                        self.pif.append(f"('{token}', '{pos}')")

                    # Check if the token is a constant
                    elif self.is_integer_constant(token):
                        if not self.symbol_table.contains_term(token):
                            pos = self.symbol_table.add(token)
                            print(f"'{token}' added to Symbol Table as a constant at position {pos}.")
                        else:
                            print(f"'{token}' is already in the Symbol Table.")
                        self.pif.append(f"('{token}', '{pos}')")

                    # Handle unrecognized tokens
                    else:
                        print(f"Lexical error at line {line_num}: Invalid token '{token}'")
                        return False

        print("Lexical analysis complete. No errors found.")
        return True


    def write_output(self, pif_file, st_file):
        with open(pif_file, "w") as file:
            for item in self.pif:
                file.write(f"{item}\n")

        with open(st_file, "w") as file:
            file.write(str(self.symbol_table.get_hash_table()))

