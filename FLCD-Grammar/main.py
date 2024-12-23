from Grammar import Grammar


def main():
    grammar = Grammar()

    grammar_file = "g1.txt".strip()
    grammar.read_from_file(grammar_file)

    grammar.print_grammar()

    while True:
        nonterminal = input("\nEnter a nonterminal to view its productions (or 'exit' to quit): ").strip()
        if nonterminal.lower() == 'exit':
            break
        productions = grammar.get_productions(nonterminal)
        if productions:
            print(f"Productions for {nonterminal}: {productions}")
        else:
            print(f"No productions found for {nonterminal}.")


if __name__ == "__main__":
    main()
