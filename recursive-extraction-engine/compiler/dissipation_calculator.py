"""
Dissipation Calculator for Controlled Rupture Compiler

Implements the exact dissipation physics:
- λ_intrinsic for each operator (ground truth, not derived)
- Pairwise λ(i→j) = λ_j + c·|[Oi,Oj]|
- Exponential decay: D(t+1) = D(t)·exp(-λ_eff)
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple


class DissipationCalculator:
    """Calculate dissipation coefficients and predict decay"""

    def __init__(self, formalism_path: Path = None):
        """Load operator formalism"""
        if formalism_path is None:
            formalism_path = Path(__file__).parent / "formalism.json"

        with open(formalism_path) as f:
            self.formalism = json.load(f)

        # Extract intrinsic λ values
        self.operators = self.formalism['operators']
        self.lambda_intrinsic = {
            name: data['lambda_intrinsic']
            for name, data in self.operators.items()
        }

        # Dissipation rules
        rules = self.formalism['dissipation_rules']
        self.c = rules['pairwise_interaction_coefficient']  # 0.15
        self.max_interaction = rules['max_interaction_magnitude']  # 0.4

        # Commutator magnitudes (will be filled from extraction)
        self.commutators = {}

    def set_commutators(self, commutator_dict: Dict[Tuple[str, str], float]):
        """
        Set commutator magnitudes from extraction.

        Args:
            commutator_dict: {(Op_i, Op_j): magnitude}
        """
        self.commutators = commutator_dict

    def lambda_pairwise(self, op_i: str, op_j: str) -> float:
        """
        Calculate λ(i→j) = λ_j_intrinsic + c·|[Oi,Oj]|

        Args:
            op_i: First operator name
            op_j: Second operator name

        Returns:
            Dissipation coefficient for applying op_j after op_i
        """
        # Base dissipation from second operator
        lambda_base = self.lambda_intrinsic[op_j]

        # Commutator interaction
        commutator_mag = self.commutators.get((op_i, op_j), 0.0)
        interaction = self.c * abs(commutator_mag)

        # Cap interaction at max
        interaction = min(interaction, self.max_interaction)

        return lambda_base + interaction

    def lambda_effective(self, sequence: List[str]) -> float:
        """
        Calculate effective λ for a sequence.
        λ_eff = mean(λ(k_t → k_{t+1}))

        Args:
            sequence: List of operator names

        Returns:
            Mean pairwise dissipation
        """
        if len(sequence) < 2:
            return 0.0

        pairwise_lambdas = [
            self.lambda_pairwise(sequence[i], sequence[i+1])
            for i in range(len(sequence) - 1)
        ]

        return np.mean(pairwise_lambdas)

    def predict_decay(
        self,
        D_initial: float,
        sequence: List[str],
        steps: int = None
    ) -> np.ndarray:
        """
        Predict dissipation decay: D(t+1) = D(t)·exp(-λ_eff)

        Args:
            D_initial: Initial dissipation value
            sequence: Operator sequence
            steps: Number of steps (default: len(sequence))

        Returns:
            Array of D values over time
        """
        if steps is None:
            steps = len(sequence)

        lambda_eff = self.lambda_effective(sequence)

        # D(t) = D_0 · exp(-λ_eff · t)
        t = np.arange(steps + 1)
        D_t = D_initial * np.exp(-lambda_eff * t)

        return D_t

    def total_dissipation_cost(self, sequence: List[str]) -> float:
        """
        Total dissipation cost for a sequence.
        Sum of all pairwise λ values.

        Args:
            sequence: List of operator names

        Returns:
            Total cost
        """
        if len(sequence) < 2:
            return 0.0

        return sum(
            self.lambda_pairwise(sequence[i], sequence[i+1])
            for i in range(len(sequence) - 1)
        )

    def get_lambda_matrix(self, operators: List[str] = None) -> np.ndarray:
        """
        Build full λ matrix for all operator pairs.

        Args:
            operators: List of operator names (default: all from formalism)

        Returns:
            Matrix where entry (i,j) = λ(op_i → op_j)
        """
        if operators is None:
            operators = list(self.operators.keys())

        n = len(operators)
        matrix = np.zeros((n, n))

        for i, op_i in enumerate(operators):
            for j, op_j in enumerate(operators):
                matrix[i, j] = self.lambda_pairwise(op_i, op_j)

        return matrix

    def analyze_sequence(self, sequence: List[str]) -> Dict:
        """
        Complete analysis of a sequence.

        Returns:
            {
                'sequence': [...],
                'lambda_effective': float,
                'total_cost': float,
                'pairwise_costs': [...],
                'predicted_decay': [D0, D1, ...],
                'half_life': float
            }
        """
        lambda_eff = self.lambda_effective(sequence)
        total_cost = self.total_dissipation_cost(sequence)

        # Pairwise breakdown
        pairwise = [
            {
                'step': i,
                'transition': f"{sequence[i]} → {sequence[i+1]}",
                'lambda': self.lambda_pairwise(sequence[i], sequence[i+1])
            }
            for i in range(len(sequence) - 1)
        ]

        # Decay prediction (assume D_0 = 1.0)
        decay = self.predict_decay(1.0, sequence)

        # Half-life: t where D(t) = D_0/2
        # D(t) = exp(-λ·t) = 0.5 → t = ln(2)/λ
        half_life = np.log(2) / lambda_eff if lambda_eff > 0 else np.inf

        return {
            'sequence': sequence,
            'lambda_effective': lambda_eff,
            'total_cost': total_cost,
            'pairwise_costs': pairwise,
            'predicted_decay': decay.tolist(),
            'half_life': half_life
        }


def example_usage():
    """Example: Calculate dissipation for operator sequences"""

    calc = DissipationCalculator()

    # Example: Set some commutator magnitudes
    # (These would come from extraction in real use)
    calc.set_commutators({
        ('Meta', 'Non'): 0.8,   # High non-commutativity
        ('Ana', 'Kata'): 0.6,   # Medium
        ('Telo', 'Ortho'): 0.1, # Low
        ('Para', 'Pro'): 0.3,
    })

    # Test sequences
    sequences = [
        ['Ana', 'Meta', 'Non'],         # High dissipation
        ['Kata', 'Telo', 'Ortho'],      # Low dissipation
        ['Para', 'Pro', 'Para', 'Pro'], # Oscillating
        ['Meta', 'Meta', 'Meta'],       # Collapse risk
    ]

    print("="*60)
    print("DISSIPATION ANALYSIS")
    print("="*60)

    for seq in sequences:
        analysis = calc.analyze_sequence(seq)

        print(f"\nSequence: {' ∘ '.join(seq)}")
        print(f"  λ_eff: {analysis['lambda_effective']:.3f}")
        print(f"  Total cost: {analysis['total_cost']:.3f}")
        print(f"  Half-life: {analysis['half_life']:.2f} steps")
        print(f"  Decay: {analysis['predicted_decay'][:5]}")

    # Show λ matrix
    print("\n" + "="*60)
    print("LAMBDA MATRIX (first 5x5)")
    print("="*60)

    ops = ['Ana', 'Kata', 'Meta', 'Para', 'Non']
    matrix = calc.get_lambda_matrix(ops)

    print("\n     ", "  ".join(f"{op:5s}" for op in ops))
    for i, op_i in enumerate(ops):
        row = "  ".join(f"{matrix[i,j]:.2f}" for j in range(len(ops)))
        print(f"{op_i:5s}  {row}")


if __name__ == '__main__':
    example_usage()
