import re


class FiniteAutomaton:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transitions = {}
        self.initial_state = None
        self.final_states = []

    def read_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Read states, alphabet, transitions, initial state, and final states
        self.states = re.findall(r"States: (.+)", lines[0])[0].split(', ')
        self.alphabet = re.findall(r"Alphabet: (.+)", lines[1])[0].split(', ')
        transition_lines = re.findall(r"(\w+) --(\w+)--> (\w+)", "".join(lines[2:]))
        for from_state, symbol, to_state in transition_lines:
            if from_state not in self.transitions:
                self.transitions[from_state] = {}
            self.transitions[from_state][symbol] = to_state
        self.initial_state = re.findall(r"Initial State: (\w+)", lines[-2])[0]
        self.final_states = re.findall(r"Final States: (.+)", lines[-1])[0].split(', ')

    def display(self):
        print("States:", ", ".join(self.states))
        print("Alphabet:", ", ".join(self.alphabet))
        print("Transitions:")
        for state, transitions in self.transitions.items():
            for symbol, next_state in transitions.items():
                print(f"  {state} --{symbol}--> {next_state}")
        print("Initial State:", self.initial_state)
        print("Final States:", ", ".join(self.final_states))

    def accepts(self, sequence):
        state = self.initial_state
        for symbol in sequence:
            if state in self.transitions and symbol in self.transitions[state]:
                state = self.transitions[state][symbol]
            else:
                return False
        return state in self.final_states


# Function to detect tokens (identifier and integer constant)
def detect_tokens(sequence):
    identifier_automaton = FiniteAutomaton()
    integer_automaton = FiniteAutomaton()

    # Define identifier DFA
    identifier_automaton.states = ['q0', 'q1', 'q_accept']
    identifier_automaton.initial_state = 'q0'
    identifier_automaton.final_states = ['q_accept']
    identifier_automaton.transitions = {
        'q0': {'a': 'q1', 'b': 'q1', 'c': 'q1', '_': 'q1'},
        'q1': {'a': 'q1', 'b': 'q1', 'c': 'q1', '0': 'q1', '1': 'q1', '9': 'q1', '_': 'q1'}
    }

    # Define integer constant DFA
    integer_automaton.states = ['q0', 'q1', 'q2', 'q_accept']
    integer_automaton.initial_state = 'q0'
    integer_automaton.final_states = ['q_accept']
    integer_automaton.transitions = {
        'q0': {'+': 'q1', '-': 'q1', '0': 'q2', '1': 'q2', '9': 'q2'},
        'q1': {'0': 'q2', '1': 'q2', '9': 'q2'},
        'q2': {'0': 'q2', '1': 'q2', '9': 'q2'}
    }

    # Now, check if the sequence matches identifier or integer constant
    if identifier_automaton.accepts(sequence):
        return "Identifier"
    elif integer_automaton.accepts(sequence):
        return "Integer Constant"
    else:
        return "Invalid Token"


def display_menu():
    print("\n--- Finite Automaton Interaction Menu ---")
    print("Please select an option from the menu below:")
    print("  1. View States")
    print("  2. View Alphabet")
    print("  3. View Transition Rules")
    print("  4. View Initial State")
    print("  5. View Final States")
    print("  6. Test a Sequence")
    print("  7. Exit Program")

def main():
    fa = FiniteAutomaton()
    fa.read_from_file('FA.in')

    while True:
        display_menu()

        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            print("\n--- Finite Automaton States ---")
            print("States:", ", ".join(fa.states))
        elif choice == '2':
            print("\n--- Finite Automaton Alphabet ---")
            print("Alphabet:", ", ".join(fa.alphabet))
        elif choice == '3':
            print("\n--- Finite Automaton Transitions ---")
            for state, transitions in fa.transitions.items():
                for symbol, next_state in transitions.items():
                    print(f"  {state} --{symbol}--> {next_state}")
        elif choice == '4':
            print("\n--- Initial State of the Automaton ---")
            print("Initial State:", fa.initial_state)
        elif choice == '5':
            print("\n--- Final States of the Automaton ---")
            print("Final States:", ", ".join(fa.final_states))
        elif choice == '6':
            sequence = input("\nEnter a sequence to check acceptance: ")
            if fa.accepts(sequence):
                print(f"The sequence '{sequence}' is accepted by the automaton.")
            else:
                print(f"The sequence '{sequence}' is NOT accepted by the automaton.")
        elif choice == '7':
            print("Thank you for using the Finite Automaton program. Exiting now.")
            break
        else:
            print("Invalid selection. Please enter a number between 1 and 7.")


if __name__ == '__main__':
    main()