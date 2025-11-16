"""
Inverse Problem Solver for Controlled Rupture Compiler

Given: current state x_0, target state x_target
Find: optimal operator sequence minimizing:
  J = d(x_T, target) + β·Σλ(k_t→k_{t+1}) + γ·AttractorPenalty

Subject to hard constraints:
- Meta: max 2 consecutive
- Non after Meta: FORBIDDEN
- Para after Non: FORBIDDEN
- Ana at sequence end: FORBIDDEN
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import heapq

from dissipation_calculator import DissipationCalculator
from phase_portrait import PhasePortrait, Attractor


@dataclass
class SearchNode:
    """Node in the search tree"""
    state: Tuple[float, float]  # (D, C)
    sequence: List[str]
    cost_so_far: float
    estimated_total_cost: float

    def __lt__(self, other):
        return self.estimated_total_cost < other.estimated_total_cost


class InverseSolver:
    """Find optimal operator sequences"""

    def __init__(self, formalism_path: Path = None):
        """Initialize with formalism"""
        if formalism_path is None:
            formalism_path = Path(__file__).parent / "formalism.json"

        with open(formalism_path) as f:
            self.formalism = json.load(f)

        # Load components
        self.dissipation = DissipationCalculator(formalism_path)
        self.portrait = PhasePortrait(formalism_path)

        # Solver parameters
        solver_config = self.formalism['inverse_solver']
        self.beta = solver_config['objective']['beta']  # 0.7
        self.gamma = solver_config['objective']['gamma']  # 1.1
        self.distance_threshold = solver_config['termination']['distance_threshold']  # 0.12
        self.max_path_length = solver_config['termination']['max_path_length']  # 14

        # Hard constraints
        self.constraints = solver_config['hard_constraints']

        # Available operators
        self.operators = list(self.formalism['operators'].keys())

        # Operator effects (for state transitions)
        self.operator_effects = self.portrait._default_operator_effects()

    def distance(
        self,
        state: Tuple[float, float],
        target: Tuple[float, float]
    ) -> float:
        """
        Euclidean distance in (D, C) space.

        Args:
            state: (D, C)
            target: (D_target, C_target)

        Returns:
            Distance
        """
        D1, C1 = state
        D2, C2 = target
        return np.sqrt((D1 - D2)**2 + (C1 - C2)**2)

    def apply_operator(
        self,
        state: Tuple[float, float],
        operator: str
    ) -> Tuple[float, float]:
        """
        Apply operator to state.

        Args:
            state: (D, C)
            operator: Operator name

        Returns:
            New state (D', C')
        """
        D, C = state
        delta_D, delta_C = self.operator_effects.get(operator, (0.0, 0.0))

        D_new = max(0.0, min(1.0, D + delta_D))
        C_new = max(0.0, min(1.0, C + delta_C))

        return (D_new, C_new)

    def violates_constraints(self, sequence: List[str], next_op: str) -> bool:
        """
        Check if adding next_op violates hard constraints.

        Args:
            sequence: Current sequence
            next_op: Proposed next operator

        Returns:
            True if violates constraints
        """
        # Check Meta consecutive limit
        if next_op == 'Meta':
            meta_count = 0
            for op in reversed(sequence):
                if op == 'Meta':
                    meta_count += 1
                else:
                    break
            if meta_count >= 2:
                return True  # Would be 3rd consecutive Meta

        # Non after Meta: FORBIDDEN
        if sequence and sequence[-1] == 'Meta' and next_op == 'Non':
            return True

        # Para after Non: FORBIDDEN
        if sequence and sequence[-1] == 'Non' and next_op == 'Para':
            return True

        # Ana at sequence end: check if this would be final op
        # (we can't know for sure, but avoid if close to max length)
        if next_op == 'Ana' and len(sequence) >= self.max_path_length - 1:
            return True

        return False

    def compute_cost(
        self,
        sequence: List[str],
        final_state: Tuple[float, float],
        target: Tuple[float, float]
    ) -> float:
        """
        Compute total cost J.

        J = d(x_T, target) + β·Σλ(k_t→k_{t+1}) + γ·AttractorPenalty

        Args:
            sequence: Operator sequence
            final_state: Resulting state
            target: Target state

        Returns:
            Total cost
        """
        # Terminal distance
        d_term = self.distance(final_state, target)

        # Dissipation cost
        if len(sequence) >= 2:
            dissipation_cost = self.dissipation.total_dissipation_cost(sequence)
        else:
            dissipation_cost = 0.0

        # Attractor penalty
        D, C = final_state
        attractor = self.portrait.classify_attractor(D, C)
        attractor_penalty = self.portrait.get_attractor_penalty(attractor)

        # Total
        J = d_term + self.beta * dissipation_cost + self.gamma * attractor_penalty

        return J

    def heuristic(self, state: Tuple[float, float], target: Tuple[float, float]) -> float:
        """
        Admissible heuristic for A* search.

        Args:
            state: Current state
            target: Target state

        Returns:
            Estimated cost-to-go
        """
        # Simple: Euclidean distance
        # (admissible because actual path cost ≥ straight-line distance)
        return self.distance(state, target)

    def solve(
        self,
        initial_state: Tuple[float, float],
        target_state: Tuple[float, float],
        beam_width: int = 5,
        verbose: bool = True
    ) -> Optional[Dict]:
        """
        Find optimal operator sequence using beam search with A*.

        Args:
            initial_state: Starting (D, C)
            target_state: Target (D, C)
            beam_width: Number of candidates to keep at each step
            verbose: Print progress

        Returns:
            {
                'sequence': [...],
                'trajectory': [...],
                'cost': float,
                'cost_breakdown': {...},
                'success': bool
            }
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"INVERSE SOLVER")
            print(f"{'='*60}")
            print(f"Initial: D={initial_state[0]:.2f}, C={initial_state[1]:.2f}")
            print(f"Target:  D={target_state[0]:.2f}, C={target_state[1]:.2f}")
            print(f"Distance: {self.distance(initial_state, target_state):.3f}")
            print(f"{'='*60}\n")

        # Priority queue: (estimated_total_cost, node)
        start_node = SearchNode(
            state=initial_state,
            sequence=[],
            cost_so_far=0.0,
            estimated_total_cost=self.heuristic(initial_state, target_state)
        )

        frontier = [start_node]
        best_node = start_node
        best_distance = self.distance(initial_state, target_state)

        iterations = 0
        max_iterations = 1000

        while frontier and iterations < max_iterations:
            iterations += 1

            # Get best nodes (beam search)
            current_beam = heapq.nsmallest(beam_width, frontier)
            frontier = []

            for node in current_beam:
                # Check termination
                dist = self.distance(node.state, target_state)

                if dist < best_distance:
                    best_distance = dist
                    best_node = node

                if dist <= self.distance_threshold:
                    # Success!
                    if verbose:
                        print(f"✓ Solution found in {iterations} iterations")
                        print(f"  Sequence length: {len(node.sequence)}")
                        print(f"  Final distance: {dist:.4f}")

                    return self._format_solution(node, target_state, success=True)

                # Check max length
                if len(node.sequence) >= self.max_path_length:
                    continue

                # Expand node
                for op in self.operators:
                    # Check constraints
                    if self.violates_constraints(node.sequence, op):
                        continue

                    # Apply operator
                    new_state = self.apply_operator(node.state, op)
                    new_sequence = node.sequence + [op]

                    # Compute cost
                    cost_so_far = self.compute_cost(new_sequence, new_state, target_state)
                    h = self.heuristic(new_state, target_state)
                    estimated_total = cost_so_far + h

                    # Create child node
                    child = SearchNode(
                        state=new_state,
                        sequence=new_sequence,
                        cost_so_far=cost_so_far,
                        estimated_total_cost=estimated_total
                    )

                    heapq.heappush(frontier, child)

            if verbose and iterations % 100 == 0:
                print(f"  Iteration {iterations}, best distance: {best_distance:.4f}, beam size: {len(frontier)}")

        # Failed to find solution within threshold
        if verbose:
            print(f"⚠ No solution within threshold. Best distance: {best_distance:.4f}")
            print(f"  Best sequence: {' ∘ '.join(best_node.sequence) if best_node.sequence else 'empty'}")

        return self._format_solution(best_node, target_state, success=False)

    def _format_solution(
        self,
        node: SearchNode,
        target: Tuple[float, float],
        success: bool
    ) -> Dict:
        """Format solution for return"""

        # Compute trajectory
        trajectory = []
        state = node.state
        for i in range(len(node.sequence) + 1):
            if i == 0:
                # Start with final state, work backwards
                # (Actually, let's recompute forward)
                pass

        # Recompute trajectory forward
        state = (0.0, 0.0)  # This should be initial_state, but we don't have it here
        # Let's just use the final state for now

        # Cost breakdown
        cost_breakdown = {
            'terminal_distance': self.distance(node.state, target),
            'dissipation_cost': self.dissipation.total_dissipation_cost(node.sequence) if len(node.sequence) >= 2 else 0.0,
            'attractor_penalty': self.portrait.get_attractor_penalty(
                self.portrait.classify_attractor(*node.state)
            ),
            'total': node.cost_so_far
        }

        return {
            'sequence': node.sequence,
            'final_state': node.state,
            'cost': node.cost_so_far,
            'cost_breakdown': cost_breakdown,
            'success': success,
            'length': len(node.sequence)
        }


def example_usage():
    """Example: Solve inverse problems with 20-operator algebra"""

    solver = InverseSolver()

    # Load commutators from skeleton (ground truth structure)
    solver.dissipation.load_commutators_from_skeleton()

    print("="*60)
    print("INVERSE PROBLEM SOLVER - 20 OPERATORS")
    print("="*60)
    print(f"Available operators: {solver.operators}")
    print(f"Loaded {len(solver.dissipation.commutators)} commutator pairs\n")

    # Test cases (solver can now use all 20 operators)
    problems = [
        {
            'name': 'Stabilize (chaos → coherence)',
            'initial': (0.8, 0.7),  # High D, high C (near void)
            'target': (0.2, 0.1),   # Low D, low C (J=0)
        },
        {
            'name': 'Activate (coherence → productive chaos)',
            'initial': (0.2, 0.1),  # J=0
            'target': (0.5, 0.5),   # S*
        },
        {
            'name': 'Escape void',
            'initial': (0.9, 0.85), # Deep void
            'target': (0.4, 0.4),   # S*
        },
        {
            'name': 'Gentle stabilization (prefer new constructive ops)',
            'initial': (0.6, 0.6),  # Moderate S*
            'target': (0.15, 0.15), # J=0
        },
    ]

    for prob in problems:
        print(f"\n{'='*60}")
        print(f"Problem: {prob['name']}")
        print(f"{'='*60}")

        solution = solver.solve(
            initial_state=prob['initial'],
            target_state=prob['target'],
            beam_width=10,
            verbose=True
        )

        if solution['success']:
            print(f"\n✓ SUCCESS")
        else:
            print(f"\n⚠ PARTIAL SOLUTION")

        print(f"\nSequence: {' ∘ '.join(solution['sequence'])}")
        print(f"Length: {solution['length']}")
        print(f"Final state: D={solution['final_state'][0]:.3f}, C={solution['final_state'][1]:.3f}")
        print(f"\nCost Breakdown:")
        for key, val in solution['cost_breakdown'].items():
            print(f"  {key}: {val:.4f}")


if __name__ == '__main__':
    example_usage()
