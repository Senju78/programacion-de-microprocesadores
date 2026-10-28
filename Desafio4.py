from typing import Set, Dict, Tuple, List

class State:
    _id_counter = 0

    def __init__(self):
        self.id = State._id_counter
        State._id_counter += 1
        self.transitions: Dict[str, List['State']] = {}

    def add_transition(self, symbol: str, target_state: 'State'):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(target_state)

    def __repr__(self):
        return f"q{self.id}"

class ThompsonNFA:
    EPSILON = 'ε'

    def __init__(self, start: State, accept: State):
        self.start = start
        self.accept = accept

    @staticmethod
    def build_symbol(symbol: str) -> 'ThompsonNFA':
        start = State()
        accept = State()
        start.add_transition(symbol, accept)
        return ThompsonNFA(start, accept)

    @staticmethod
    def build_union(nfa1: 'ThompsonNFA', nfa2: 'ThompsonNFA') -> 'ThompsonNFA':
        start = State()
        accept = State()
        start.add_transition(ThompsonNFA.EPSILON, nfa1.start)
        start.add_transition(ThompsonNFA.EPSILON, nfa2.start)
        nfa1.accept.add_transition(ThompsonNFA.EPSILON, accept)
        nfa2.accept.add_transition(ThompsonNFA.EPSILON, accept)
        return ThompsonNFA(start, accept)

    @staticmethod
    def build_concat(nfa1: 'ThompsonNFA', nfa2: 'ThompsonNFA') -> 'ThompsonNFA':
        nfa1.accept.add_transition(ThompsonNFA.EPSILON, nfa2.start)
        return ThompsonNFA(nfa1.start, nfa2.accept)

    @staticmethod
    def build_kleene(nfa: 'ThompsonNFA') -> 'ThompsonNFA':
        start = State()
        accept = State()
        start.add_transition(ThompsonNFA.EPSILON, accept)
        start.add_transition(ThompsonNFA.EPSILON, nfa.start)
        nfa.accept.add_transition(ThompsonNFA.EPSILON, accept)
        nfa.accept.add_transition(ThompsonNFA.EPSILON, nfa.start)
        return ThompsonNFA(start, accept)

    @staticmethod
    def build_optional(nfa: 'ThompsonNFA') -> 'ThompsonNFA':
        start = State()
        accept = State()
        start.add_transition(ThompsonNFA.EPSILON, nfa.start)
        start.add_transition(ThompsonNFA.EPSILON, accept)
        nfa.accept.add_transition(ThompsonNFA.EPSILON, accept)
        return ThompsonNFA(start, accept)

    def print_nfa(self):
        visited = set()
        stack = [self.start]
        print(f"\n=== AFN Thompson (Inicio: {self.start}, Aceptación: {self.accept}) ===")
        while stack:
            state = stack.pop()
            if state.id in visited:
                continue
            visited.add(state.id)
            for symbol, targets in state.transitions.items():
                for target in targets:
                    print(f"  {state} --({symbol})--> {target}")
                    if target.id not in visited:
                        stack.append(target)

if __name__ == "__main__":
    print("Expresión: a?")
    State._id_counter = 0
    nfa_a = ThompsonNFA.build_symbol('a')
    nfa_opt = ThompsonNFA.build_optional(nfa_a)
    nfa_opt.print_nfa()

    print("\nExpresión: (aa)?")
    State._id_counter = 0
    nfa_a1 = ThompsonNFA.build_symbol('a')
    nfa_a2 = ThompsonNFA.build_symbol('a')
    nfa_aa = ThompsonNFA.build_concat(nfa_a1, nfa_a2)
    nfa_aa_opt = ThompsonNFA.build_optional(nfa_aa)
    nfa_aa_opt.print_nfa()
