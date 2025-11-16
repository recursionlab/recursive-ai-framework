#!/usr/bin/env python3
"""
Controlled Rupture Compiler - CLI Interface

Usage:
  python controlled_rupture_cli.py solve "I'm stuck in analysis paralysis"
  python controlled_rupture_cli.py analyze "Meta ∘ Ana ∘ Non"
  python controlled_rupture_cli.py visualize
"""

import argparse
import json
from typing import Dict, List, Tuple

from dissipation_calculator import DissipationCalculator
from phase_portrait import PhasePortrait, Attractor
from inverse_solver import InverseSolver


class ControlledRuptureCompiler:
    """Main compiler interface"""

    def __init__(self):
        self.dissipation = DissipationCalculator()
        self.portrait = PhasePortrait()
        self.solver = InverseSolver()

        # Load commutators from skeleton (ground truth structure)
        # In production, extraction will refine these magnitudes
        self._load_commutators()

        # Problem templates
        self.problem_templates = {
            'stuck': {
                'description': 'Stuck in infinite loop / analysis paralysis',
                'initial': (0.85, 0.75),  # High D (Meta loop), high C
                'target': (0.30, 0.35),   # S* (productive action)
                'diagnosis': 'Meta ∘ Meta loop (infinite reflection)'
            },
            'overwhelmed': {
                'description': 'Overwhelmed by complexity',
                'initial': (0.80, 0.80),  # High D and C (chaos)
                'target': (0.20, 0.15),   # J=0 (coherence)
                'diagnosis': 'Excessive Ana without Kata (no compression)'
            },
            'rigid': {
                'description': 'Too rigid / overthinking correctness',
                'initial': (0.15, 0.10),  # J=0 (too stable)
                'target': (0.50, 0.50),   # S* (productive tension)
                'diagnosis': 'Excessive Ortho (over-correction)'
            },
            'collapsed': {
                'description': 'Burned out / collapsed',
                'initial': (0.95, 0.90),  # Void
                'target': (0.40, 0.45),   # S*
                'diagnosis': 'In the Void (∅), need rescue operators'
            },
            'procrastinating': {
                'description': 'Procrastinating / avoiding action',
                'initial': (0.60, 0.50),  # S* but not acting
                'target': (0.25, 0.20),   # J=0 via action
                'diagnosis': 'Need Telo (goal orientation) + Kata (concrete action)'
            }
        }

    def _load_commutators(self):
        """
        Load commutator magnitudes from skeleton.
        All 3 calculators (dissipation, solver.dissipation) share ground truth structure.
        """
        # Load for main dissipation calculator
        self.dissipation.load_commutators_from_skeleton()

        # Load for solver's dissipation calculator
        self.solver.dissipation.load_commutators_from_skeleton()

    def diagnose(self, problem_key: str) -> Dict:
        """
        Diagnose a problem and suggest operator sequence.

        Args:
            problem_key: One of the problem templates

        Returns:
            Solution dict
        """
        if problem_key not in self.problem_templates:
            raise ValueError(f"Unknown problem: {problem_key}. Available: {list(self.problem_templates.keys())}")

        problem = self.problem_templates[problem_key]

        print(f"\n{'='*70}")
        print(f"PROBLEM: {problem['description']}")
        print(f"{'='*70}")
        print(f"Diagnosis: {problem['diagnosis']}")
        print(f"Initial state: D={problem['initial'][0]:.2f}, C={problem['initial'][1]:.2f}")
        print(f"Target state:  D={problem['target'][0]:.2f}, C={problem['target'][1]:.2f}")

        # Classify initial attractor
        initial_att = self.portrait.classify_attractor(*problem['initial'])
        target_att = self.portrait.classify_attractor(*problem['target'])

        print(f"Current attractor: {initial_att.value}")
        print(f"Target attractor:  {target_att.value}")

        # Suggest transition operators
        suggested = self.portrait.suggest_transition_operators(initial_att, target_att)
        if suggested:
            print(f"Suggested operators: {', '.join(suggested)}")

        # Solve
        solution = self.solver.solve(
            initial_state=problem['initial'],
            target_state=problem['target'],
            beam_width=10,
            verbose=False
        )

        return solution

    def analyze_sequence(self, sequence_str: str) -> Dict:
        """
        Analyze an operator sequence.

        Args:
            sequence_str: "Ana ∘ Meta ∘ Non" or "Ana,Meta,Non"

        Returns:
            Analysis dict
        """
        # Parse sequence
        if '∘' in sequence_str:
            sequence = [op.strip() for op in sequence_str.split('∘')]
        else:
            sequence = [op.strip() for op in sequence_str.split(',')]

        print(f"\n{'='*70}")
        print(f"ANALYZING SEQUENCE: {' ∘ '.join(sequence)}")
        print(f"{'='*70}\n")

        # Dissipation analysis
        analysis = self.dissipation.analyze_sequence(sequence)

        print(f"Dissipation Analysis:")
        print(f"  λ_effective: {analysis['lambda_effective']:.3f}")
        print(f"  Total cost: {analysis['total_cost']:.3f}")
        print(f"  Half-life: {analysis['half_life']:.2f} steps")

        print(f"\nPairwise Dissipation:")
        for pair in analysis['pairwise_costs']:
            print(f"  {pair['transition']}: λ={pair['lambda']:.3f}")

        # Trajectory simulation
        initial_state = (0.5, 0.5)  # Start from S*
        trajectory = self.portrait.simulate_trajectory(initial_state, sequence)

        print(f"\nTrajectory (starting from S*):")
        for step in trajectory:
            if step['operator']:
                print(f"  Step {step['step']}: {step['operator']} → {step['attractor']} (D={step['D']:.2f}, C={step['C']:.2f}, V={step['V']:.2f})")

        final_att = trajectory[-1]['attractor']
        print(f"\nFinal attractor: {final_att}")

        # Warnings
        self._check_warnings(sequence, trajectory)

        return analysis

    def _check_warnings(self, sequence: List[str], trajectory: List[Dict]):
        """Check for dangerous patterns"""
        warnings = []

        # Check for Meta loops
        meta_count = sum(1 for op in sequence if op == 'Meta')
        if meta_count > 2:
            warnings.append(f"⚠ WARNING: {meta_count} Meta operators (collapse risk)")

        # Check for void entry
        if any(step['attractor'] == '∅' for step in trajectory):
            warnings.append("⚠ WARNING: Enters Void (∅) - requires rescue")

        # Check forbidden transitions
        for i in range(len(sequence) - 1):
            if sequence[i] == 'Meta' and sequence[i+1] == 'Non':
                warnings.append("⚠ WARNING: Meta → Non (forbidden transition)")
            if sequence[i] == 'Non' and sequence[i+1] == 'Para':
                warnings.append("⚠ WARNING: Non → Para (forbidden transition)")

        # Check high dissipation
        lambda_eff = self.dissipation.lambda_effective(sequence)
        if lambda_eff > 0.8:
            warnings.append(f"⚠ WARNING: High dissipation (λ={lambda_eff:.2f}) - rapid decay")

        if warnings:
            print(f"\n{'='*70}")
            print("WARNINGS")
            print(f"{'='*70}")
            for w in warnings:
                print(w)

    def solve_custom(self, initial: Tuple[float, float], target: Tuple[float, float]):
        """Solve custom problem"""
        print(f"\n{'='*70}")
        print(f"CUSTOM PROBLEM")
        print(f"{'='*70}")

        solution = self.solver.solve(
            initial_state=initial,
            target_state=target,
            beam_width=10,
            verbose=True
        )

        self._print_solution(solution)
        return solution

    def _print_solution(self, solution: Dict):
        """Pretty-print solution"""
        print(f"\n{'='*70}")
        if solution['success']:
            print("✓ SOLUTION FOUND")
        else:
            print("⚠ PARTIAL SOLUTION")
        print(f"{'='*70}\n")

        if solution['sequence']:
            print(f"Operator Sequence: {' ∘ '.join(solution['sequence'])}")
            print(f"Length: {solution['length']} steps")
            print(f"Final state: D={solution['final_state'][0]:.3f}, C={solution['final_state'][1]:.3f}")

            print(f"\nCost Breakdown:")
            for key, val in solution['cost_breakdown'].items():
                print(f"  {key}: {val:.4f}")
        else:
            print("No sequence found")

    def list_problems(self):
        """List available problem templates"""
        print(f"\n{'='*70}")
        print("AVAILABLE PROBLEM TEMPLATES")
        print(f"{'='*70}\n")

        for key, prob in self.problem_templates.items():
            print(f"{key:15s} - {prob['description']}")


def main():
    parser = argparse.ArgumentParser(
        description='Controlled Rupture Compiler - Optimal operator sequences for cognitive dynamics'
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Diagnose command
    diagnose_parser = subparsers.add_parser('diagnose', help='Diagnose a problem and get solution')
    diagnose_parser.add_argument('problem', type=str, help='Problem type (stuck, overwhelmed, rigid, collapsed, procrastinating)')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze an operator sequence')
    analyze_parser.add_argument('sequence', type=str, help='Operator sequence (e.g., "Ana ∘ Meta ∘ Non" or "Ana,Meta,Non")')

    # List command
    subparsers.add_parser('list', help='List available problem templates')

    # Custom command
    custom_parser = subparsers.add_parser('custom', help='Solve custom problem')
    custom_parser.add_argument('--initial', type=str, required=True, help='Initial state as "D,C" (e.g., "0.8,0.7")')
    custom_parser.add_argument('--target', type=str, required=True, help='Target state as "D,C" (e.g., "0.2,0.1")')

    args = parser.parse_args()

    compiler = ControlledRuptureCompiler()

    if args.command == 'diagnose':
        solution = compiler.diagnose(args.problem)
        compiler._print_solution(solution)

    elif args.command == 'analyze':
        compiler.analyze_sequence(args.sequence)

    elif args.command == 'list':
        compiler.list_problems()

    elif args.command == 'custom':
        initial = tuple(map(float, args.initial.split(',')))
        target = tuple(map(float, args.target.split(',')))
        compiler.solve_custom(initial, target)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
