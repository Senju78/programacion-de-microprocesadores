# ==============================================================================
# Tema: Emulador de Autómata Finito Determinista (AFD) y Matriz de Transición
# ==============================================================================

from typing import Set, Dict, Tuple, List, Optional

class AutomataFinitoDeterminista:
    """Clase orientada a objetos para modelar y simular un AFD (5-tupla)."""

    def __init__(self, states: Set[int], alphabet: Set[str],
                 transitions: Dict[Tuple[int, str], int],
                 initial_state: int, accepting_states: Set[int]):
        self.S = states
        self.Sigma = alphabet
        self.delta = transitions  # Corregido: atributo asignado correctamente
        self.s0 = initial_state
        self.F = accepting_states
        
        # Estado de Error implícito
        self.ERROR_STATE = -1

    def transition(self, state: int, symbol: str) -> int:
        """Consulta la función/matriz de transición delta(s, c)."""
        return self.delta.get((state, symbol), self.ERROR_STATE) # Corregido: llamado al atributo delta

    def evaluate_string(self, input_string: str) -> Tuple[bool, List[str]]:
        """Simula la ejecución del AFD carácter a carácter trazando los estados."""
        current_state = self.s0
        trace = [f"Estado Inicial: q{current_state}"]

        for i, char in enumerate(input_string):
            if char not in self.Sigma:
                trace.append(f"  [Error] Carácter '{char}' fuera del alfabeto Sigma.")
                return False, trace

            next_state = self.transition(current_state, char)
            if next_state == self.ERROR_STATE:
                trace.append(f"  [Bloqueo] Sin transición desde q{current_state} con '{char}'.")
                return False, trace

            trace.append(f"  Paso {i+1}: Símbolo '{char}' | Transición q{current_state} -> q{next_state}")
            current_state = next_state

        is_accepted = current_state in self.F
        status = "CADENA ACEPTADA" if is_accepted else "CADENA RECHAZADA"
        trace.append(f"Estado Final: q{current_state} | Resultado: {status}")
        return is_accepted, trace

    def print_transition_matrix(self):
        """Imprime la representación tabular/matriz de transición del AFD."""
        sorted_symbols = sorted(list(self.Sigma))
        sorted_states = sorted(list(self.S))

        print("\n=== MATRIZ DE TRANSICIÓN Dtran[s, c] ===")
        header = f"{'Estado':<8} | " + " | ".join([f"{sym:^5}" for sym in sorted_symbols])
        print(header)
        print("-" * len(header))

        for state in sorted_states:
            prefix = "-> " if state == self.s0 else (" * " if state in self.F else "   ")
            row_str = f"{prefix}q{state:<4} | "
            row_cells = []
            for sym in sorted_symbols:
                dest = self.transition(state, sym)
                cell = f"q{dest}" if dest != self.ERROR_STATE else "--"
                row_cells.append(f"{cell:^5}")
            row_str += " | ".join(row_cells)
            print(row_str)

# --- DEMOSTRACIÓN PRÁCTICA Y EVALUACIÓN ---
if __name__ == "__main__":
    # AFD para reconocer DOS cosas:
    #   1) identificadores   ->  L (L | D)*
    #   2) enteros positivos ->  D+   (uno o mas digitos)      [NUEVO en el Desafio 1]

    states_set = {0, 1, 2}   # q0 = inicio | q1 = identificador | q2 = numero entero (q2 es NUEVO)
    alphabet_set = {'L', 'D'}

    # Transiciones:
    # q0 --L--> q1
    # q1 --L--> q1
    # q1 --D--> q1
    # q0 --D--> q2   (NUEVA)
    # q2 --D--> q2   (NUEVA)
    transitions_map = {
        (0, 'L'): 1,
        (1, 'L'): 1,
        (1, 'D'): 1,
        (0, 'D'): 2,   # NUEVA: si empiezo con un digito, voy a q2
        (2, 'D'): 2    # NUEVA: en q2 sigo con mas digitos
    }

    initial = 0
    accepting = {1, 2}   # CAMBIO: q1 (identificador) y q2 (numero) aceptan

    afd_id = AutomataFinitoDeterminista(states_set, alphabet_set, transitions_map, initial, accepting)

    # Mostrar la matriz de transición
    afd_id.print_transition_matrix()

    # Batería de pruebas
    test_inputs = [
        # --- Cadenas originales del profesor ---
        "LLD",    # -> 'LLL': q0-L->q1, q1-L->q1, q1-L->q1; fin en q1 (acepta) -> ACEPTADA
        "L1D",    # -> 'LDL': q0-L->q1, q1-D->q1, q1-L->q1; fin en q1 -> ACEPTADA
        "DLL",    # OJO: la 'D' es una LETRA para Python -> 'LLL' -> ACEPTADA (no es un digito real)
        "L",      # q0-L->q1; fin en q1 -> ACEPTADA
        # --- 3 cadenas NUEVAS del Desafio 1 ---
        # 1) VALIDA que empieza con digitos: "2026" -> 'DDDD'
        #    Paso 1: q0 --D--> q2 (flecha NUEVA).  Pasos 2, 3 y 4: q2 --D--> q2.
        #    Termina en q2, que es de aceptacion -> ACEPTADA (es un entero positivo, D+).
        "2026",
        # 2) MIXTA (empieza con digitos y luego una letra): "12a" -> 'DDL'
        #    Pasos 1 y 2: q0 --D--> q2 y q2 --D--> q2.
        #    Paso 3: desde q2 con 'L' NO hay flecha -> [Bloqueo] -> RECHAZADA.
        "12a",
        # 3) INVALIDA (simbolo fuera del alfabeto): "a-b" -> 'L-L'
        #    Paso 1: q0 --L--> q1.
        #    Paso 2: '-' no esta en Sigma = {L, D} -> [Error] -> RECHAZADA.
        "a-b"
    ]

    print("\n=== EVALUACIÓN DE CADENAS DE PRUEBA ===")
    for test in test_inputs:
        # Convertir caracteres para simplificar la prueba (letras -> 'L', dígitos -> 'D')
        mapped_input = "".join(['L' if c.isalpha() else ('D' if c.isdigit() else c) for c in test])
        print(f"\nEvaluating Input Original: '{test}' -> Abstract: '{mapped_input}'")
        accepted, execution_trace = afd_id.evaluate_string(mapped_input)
        for line in execution_trace:
            print(line)
