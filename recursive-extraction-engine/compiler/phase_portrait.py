"""
Phase Portrait Engine for Controlled Rupture Compiler

Implements the exact attractor topology:
- 3 attractors: J=0, S*, ∅
- Fixed transition rules
- Lyapunov function V(x) = D(x) + α·C(x)
- Basin identification
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from enum import Enum


class Attractor(Enum):
    """The three attractor types"""
    J_EQUALS_0 = "J=0"      # Coherent equilibrium
    S_STAR = "S*"           # Productive contradiction
    VOID = "∅"              # Collapse


class PhasePortrait:
    """Phase portrait dynamics and attractor topology"""

    def __init__(self, formalism_path: Path = None):
        """Load formalism"""
        if formalism_path is None:
            formalism_path = Path(__file__).parent / "formalism.json"

        with open(formalism_path) as f:
            self.formalism = json.load(f)

        # Extract attractor data
        self.attractors = self.formalism['phase_portrait']['attractors']
        self.transitions = self.formalism['phase_portrait']['transitions']
        self.lyapunov = self.formalism['phase_portrait']['lyapunov']

        self.alpha = self.lyapunov['alpha']  # 0.4
        self.stability_threshold = self.lyapunov['stability_condition'].split('<')[1].strip()
        self.stability_threshold = float(self.stability_threshold)  # 0.3

    def lyapunov_function(self, D: float, C: float) -> float:
        """
        V(x) = D(x) + α·C(x)

        Args:
            D: Dissipation measure
            C: Contradiction curvature

        Returns:
            Lyapunov value
        """
        return D + self.alpha * C

    def classify_attractor(self, D: float, C: float) -> Attractor:
        """
        Classify state into attractor based on Lyapunov function.

        Args:
            D: Dissipation
            C: Contradiction curvature

        Returns:
            Attractor type
        """
        V = self.lyapunov_function(D, C)

        # J=0: Low dissipation, stable
        if V < self.stability_threshold:
            return Attractor.J_EQUALS_0

        # Void: Very high dissipation or contradiction
        if D > 0.8 or C > 0.9:
            return Attractor.VOID

        # S*: Everything else (productive contradiction region)
        return Attractor.S_STAR

    def can_transition(
        self,
        from_attractor: Attractor,
        to_attractor: Attractor,
        operators: List[str]
    ) -> bool:
        """
        Check if operator sequence can transition between attractors.

        Args:
            from_attractor: Starting attractor
            to_attractor: Target attractor
            operators: Operator sequence

        Returns:
            True if transition is possible
        """
        # Build transition key
        key = f"{from_attractor.value}_to_{to_attractor.value.replace('=', '').replace('*', '_star').replace('∅', 'void')}"

        # Get required operators for this transition
        required = self.transitions.get(key, [])

        if not required:
            return False

        # Check if ALL required operators are present
        operators_set = set(operators)
        return all(op in operators_set for op in required)

    def suggest_transition_operators(
        self,
        from_attractor: Attractor,
        to_attractor: Attractor
    ) -> List[str]:
        """
        Suggest operators to transition between attractors.
        Now includes all 20 operators for richer suggestions.

        Returns:
            List of required operators
        """
        transition_map = {
            # Stabilizing transitions (→ J=0)
            (Attractor.S_STAR, Attractor.J_EQUALS_0): ['Kata', 'Telo', 'Seed', 'Latch'],
            (Attractor.VOID, Attractor.J_EQUALS_0): ['Telo', 'Kata', 'Axis', 'Bind'],

            # Activating transitions (→ S*)
            (Attractor.J_EQUALS_0, Attractor.S_STAR): ['Para', 'Ana', 'Crux', 'Echo'],
            (Attractor.VOID, Attractor.S_STAR): ['Pro', 'Ortho', 'Weave', 'Seed'],

            # Destabilizing transitions (→ ∅)
            (Attractor.S_STAR, Attractor.VOID): ['Non', 'Meta', 'Vale', 'Fold'],
            (Attractor.J_EQUALS_0, Attractor.VOID): ['Non', 'Vale', 'Flux'],
        }

        return transition_map.get((from_attractor, to_attractor), [])

    def get_attractor_penalty(self, attractor: Attractor) -> float:
        """
        Get penalty for being in a particular attractor.

        Args:
            attractor: Attractor type

        Returns:
            Penalty value
        """
        penalties = self.formalism['inverse_solver']['attractor_penalties']

        penalty_map = {
            Attractor.J_EQUALS_0: penalties['J_equals_0'],  # 0.1
            Attractor.S_STAR: penalties['S_star'],          # 0.3
            Attractor.VOID: penalties['void'],              # 1.0
        }

        return penalty_map[attractor]

    def simulate_trajectory(
        self,
        initial_state: Tuple[float, float],  # (D, C)
        operator_sequence: List[str],
        operator_effects: Dict[str, Tuple[float, float]] = None
    ) -> List[Dict]:
        """
        Simulate a trajectory through phase space.

        Args:
            initial_state: (D_0, C_0)
            operator_sequence: List of operators to apply
            operator_effects: {op_name: (ΔD, ΔC)} change per operator

        Returns:
            List of states: [{'step': int, 'D': float, 'C': float, 'attractor': Attractor, 'V': float}, ...]
        """
        if operator_effects is None:
            # Default effects (simplified)
            operator_effects = self._default_operator_effects()

        D, C = initial_state
        trajectory = []

        # Initial state
        attractor = self.classify_attractor(D, C)
        V = self.lyapunov_function(D, C)

        trajectory.append({
            'step': 0,
            'operator': None,
            'D': D,
            'C': C,
            'V': V,
            'attractor': attractor.value
        })

        # Apply operators
        for step, op in enumerate(operator_sequence, 1):
            delta_D, delta_C = operator_effects.get(op, (0.0, 0.0))

            D = max(0.0, min(1.0, D + delta_D))  # Clamp to [0,1]
            C = max(0.0, min(1.0, C + delta_C))

            attractor = self.classify_attractor(D, C)
            V = self.lyapunov_function(D, C)

            trajectory.append({
                'step': step,
                'operator': op,
                'D': D,
                'C': C,
                'V': V,
                'attractor': attractor.value
            })

        return trajectory

    def _default_operator_effects(self) -> Dict[str, Tuple[float, float]]:
        """
        Default effects of operators on (D, C).

        Operator classes guide effects:
        - A-Constructive (low λ): negative ΔD, ΔC (stabilizing)
        - B-Disruptive (high λ): positive ΔD, ΔC (destabilizing)
        - C-Reflexive (medium λ): mixed or small changes
        - D-Structural: specialized effects

        Returns:
            {operator: (ΔD, ΔC)}
        """
        return {
            # Original 9 operators
            'Ana': (0.15, 0.1),     # B-Disruptive: Increases both
            'Kata': (-0.20, -0.15), # A-Constructive: Decreases both (idempotent)
            'Meta': (0.10, 0.05),   # C-Reflexive: Slight increase
            'Para': (0.12, 0.18),   # C-Reflexive: High C increase
            'Non': (0.25, 0.20),    # B-Disruptive: Strong increase
            'Telo': (-0.18, -0.10), # A-Constructive: Decrease, stabilize (absorbing)
            'Retro': (-0.05, 0.0),  # D-Structural: Slight D decrease
            'Ortho': (-0.15, -0.12),# A-Constructive: Decrease both
            'Pro': (0.05, 0.02),    # D-Structural: Slight increase

            # New 11 operators
            'Echo': (0.08, 0.06),   # C-Reflexive (λ=0.45): Small increase, reflection
            'Braid': (0.10, 0.12),  # C-Reflexive (λ=0.55): Moderate increase, interweaving
            'Fold': (0.18, 0.14),   # B-Disruptive (λ=0.70): High increase, compression stress
            'Seed': (-0.17, -0.11), # A-Constructive (λ=0.28): Strong decrease, foundation
            'Crux': (0.07, 0.09),   # C-Reflexive (λ=0.42): Small increase, pivot point
            'Weave': (-0.16, -0.13),# A-Constructive (λ=0.33): Decrease, integration
            'Bind': (-0.14, -0.10), # A-Constructive (λ=0.38): Decrease, cohesion
            'Axis': (-0.16, -0.12), # A-Constructive (λ=0.31): Decrease, alignment
            'Vale': (0.22, 0.18),   # B-Disruptive (λ=0.88): Strong increase, deep descent
            'Flux': (0.14, 0.11),   # B-Disruptive (λ=0.60): Moderate increase, flow
            'Latch': (-0.17, -0.12),# A-Constructive (λ=0.29): Strong decrease, fixation
        }

    def analyze_basin_structure(
        self,
        num_samples: int = 1000,
        operator_sequence: List[str] = None
    ) -> Dict:
        """
        Sample phase space to estimate basin sizes.

        Args:
            num_samples: Number of random initial states
            operator_sequence: If provided, apply this sequence; else run random ops

        Returns:
            {
                'basin_sizes': {Attractor: fraction},
                'samples': [...],
                'transition_counts': {...}
            }
        """
        # Sample random initial states
        D_samples = np.random.uniform(0, 1, num_samples)
        C_samples = np.random.uniform(0, 1, num_samples)

        basin_counts = {att: 0 for att in Attractor}
        transitions = {}

        for D, C in zip(D_samples, C_samples):
            initial_att = self.classify_attractor(D, C)

            if operator_sequence:
                # Apply sequence
                traj = self.simulate_trajectory((D, C), operator_sequence)
                final_att = Attractor(traj[-1]['attractor'])
            else:
                final_att = initial_att

            basin_counts[final_att] += 1

            # Track transitions
            if initial_att != final_att:
                key = f"{initial_att.value}→{final_att.value}"
                transitions[key] = transitions.get(key, 0) + 1

        # Compute fractions
        basin_sizes = {
            att.value: count / num_samples
            for att, count in basin_counts.items()
        }

        return {
            'basin_sizes': basin_sizes,
            'transition_counts': transitions,
            'num_samples': num_samples
        }


def example_usage():
    """Example: Simulate trajectories and analyze basins"""

    portrait = PhasePortrait()

    print("="*60)
    print("PHASE PORTRAIT ANALYSIS - 20 OPERATORS")
    print("="*60)

    # Test sequences (mix of original and new operators)
    sequences = {
        'Stabilize (original)': ['Kata', 'Telo', 'Ortho'],
        'Stabilize (new)': ['Seed', 'Latch', 'Axis'],
        'Destabilize (original)': ['Ana', 'Para', 'Non'],
        'Destabilize (new)': ['Vale', 'Flux', 'Fold'],
        'Reflect': ['Echo', 'Braid', 'Crux'],
        'Collapse': ['Meta', 'Meta', 'Non'],
        'Rescue (original)': ['Pro', 'Ortho', 'Telo'],
        'Rescue (new)': ['Weave', 'Bind', 'Seed'],
    }

    for name, seq in sequences.items():
        print(f"\n{name}: {' ∘ '.join(seq)}")

        # Start from S* attractor (D=0.5, C=0.5)
        traj = portrait.simulate_trajectory((0.5, 0.5), seq)

        print(f"  Initial: {traj[0]['attractor']} (D={traj[0]['D']:.2f}, C={traj[0]['C']:.2f}, V={traj[0]['V']:.2f})")
        print(f"  Final:   {traj[-1]['attractor']} (D={traj[-1]['D']:.2f}, C={traj[-1]['C']:.2f}, V={traj[-1]['V']:.2f})")

        # Show path
        path = " → ".join([s['attractor'] for s in traj])
        print(f"  Path: {path}")

    # Basin analysis
    print("\n" + "="*60)
    print("BASIN STRUCTURE (1000 random samples)")
    print("="*60)

    basins = portrait.analyze_basin_structure(num_samples=1000)

    print("\nBasin Sizes:")
    for att, size in basins['basin_sizes'].items():
        print(f"  {att}: {size:.1%}")


if __name__ == '__main__':
    example_usage()
