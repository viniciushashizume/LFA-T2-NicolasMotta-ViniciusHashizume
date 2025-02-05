class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states, deterministic=True):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  # Dict[state][symbol] = set(next_states)
        self.start_state = start_state
        self.final_states = final_states
        self.deterministic = deterministic

    def __str__(self):
        result = f"M = ({self.alphabet}, {self.states}, δ, {self.start_state}, {self.final_states})\n"
        result += "Transições:\n"
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                result += f"  δ({state}, {symbol}) -> {', '.join(next_states)}\n"
        return result

class RegularGrammar:
    def __init__(self, automaton):
        self.non_terminals = automaton.states | {"S"}
        self.terminals = automaton.alphabet
        self.start_symbol = "S"
        self.productions = self.generate_productions(automaton)

    def generate_productions(self, automaton):
        productions = {state: [] for state in automaton.states}
        productions["S"] = [f"{automaton.start_state}"]
        
        for state, transitions in automaton.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    productions[state].append(f"{symbol}{next_state}")
        
        for final_state in automaton.final_states:
            productions[final_state].append("ε")

        return productions

    def __str__(self):
        result = f"G = ({self.non_terminals}, {self.terminals}, P, {self.start_symbol})\n"
        result += "Produções:\n"
        for non_terminal, rules in self.productions.items():
            result += f"  {non_terminal} -> " + " | ".join(rules) + "\n"
        return result

# Definição do autômato de exemplo (NFA)
states = {"q0", "q1", "q2"}
alphabet = {"a", "b", "c"}
transitions = {
    "q0": {"a": {"q1"}, "b": {"q2", "q0"}},
    "q1": {"b": {"q0"}, "c": {"q2"}},
    "q2": {"a": {"q0"}}
}
start_state = "q0"
final_states = {"q0", "q1", "q2"}

# Criando e exibindo o autômato
automaton = FiniteAutomaton(states, alphabet, transitions, start_state, final_states, deterministic=False)
print(automaton)

# Criando e exibindo a gramática correspondente
grammar = RegularGrammar(automaton)
print(grammar)
