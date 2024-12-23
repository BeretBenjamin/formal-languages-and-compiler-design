from lexical_analyzer import LexicalAnalyzer
from symbol_table import SymbolTable


class Main:
    def __init__(self):
        symbol_table = SymbolTable(5)

        symbol_table.add("1")
        print(symbol_table.contains_term("1"))
        position = symbol_table.find_position_of_term("1")
        print(position)

        symbol_table.add("6")
        print(symbol_table.contains_term("6"))
        print(symbol_table.find_position_of_term("6"))

        symbol_table.add("5")
        print(symbol_table.contains_term("5"))
        print(symbol_table.find_position_of_term("5"))
        print(symbol_table.get_hash_table())



if __name__ == "__main__":
    #Main()
    lexical_analyzer = LexicalAnalyzer("token.in")
    if lexical_analyzer.analyze("p1.txt"):
        lexical_analyzer.write_output("PIF.out", "ST.out")
