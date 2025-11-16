#!/usr/bin/env python3
"""
Comprehensive Test of 20-Operator Controlled Rupture Compiler v2.0.0

Tests all 20 operators across all components:
- Dissipation calculator
- Phase portrait
- Inverse solver
- CLI integration
"""

import json
from pathlib import Path
from dissipation_calculator import DissipationCalculator
from phase_portrait import PhasePortrait
from inverse_solver import InverseSolver
from controlled_rupture_cli import ControlledRuptureCompiler


def test_formalism_structure():
    """Verify formalism.json v2.0.0 structure"""
    print("="*70)
    print("TEST 1: Formalism Structure")
    print("="*70)

    formalism_path = Path(__file__).parent / "formalism.json"
    with open(formalism_path) as f:
        formalism = json.load(f)

    # Check metadata
    assert formalism['metadata']['version'] == '2.0.0', "Version should be 2.0.0"
    assert len(formalism['operators']) == 20, f"Should have 20 operators, got {len(formalism['operators'])}"

    # Check operator classes
    classes = {}
    for name, data in formalism['operators'].items():
        op_class = data.get('class', 'unknown')
        classes[op_class] = classes.get(op_class, 0) + 1

    print(f"✓ Version: {formalism['metadata']['version']}")
    print(f"✓ Operators: {len(formalism['operators'])}")
    print(f"✓ Operator classes:")
    for cls, count in sorted(classes.items()):
        print(f"    {cls}: {count} operators")

    # Verify all 20 operators are present
    expected_operators = [
        'Ana', 'Kata', 'Meta', 'Para', 'Non', 'Telo', 'Retro', 'Ortho', 'Pro',
        'Echo', 'Braid', 'Fold', 'Seed', 'Crux', 'Weave', 'Bind', 'Axis', 'Vale', 'Flux', 'Latch'
    ]
    actual_operators = list(formalism['operators'].keys())
    assert actual_operators == expected_operators, f"Operator list mismatch"

    print(f"✓ All 20 operators verified\n")


def test_commutator_skeleton():
    """Verify commutator_skeleton.json has 20×20 = 400 entries"""
    print("="*70)
    print("TEST 2: Commutator Skeleton")
    print("="*70)

    skeleton_path = Path(__file__).parent / "commutator_skeleton.json"
    with open(skeleton_path) as f:
        skeleton = json.load(f)

    matrix = skeleton['commutator_matrix']
    total_entries = sum(len(pairs) for pairs in matrix.values())

    assert len(matrix) == 20, f"Should have 20 rows, got {len(matrix)}"
    assert total_entries == 400, f"Should have 400 entries (20×20), got {total_entries}"

    print(f"✓ Commutator matrix: {len(matrix)}×20 = {total_entries} entries")

    # Verify each operator has 20 commutator pairs
    for op, pairs in matrix.items():
        assert len(pairs) == 20, f"{op} should have 20 pairs, got {len(pairs)}"

    print(f"✓ All operators have complete commutator definitions\n")


def test_dissipation_calculator():
    """Test dissipation calculator with all 20 operators"""
    print("="*70)
    print("TEST 3: Dissipation Calculator")
    print("="*70)

    calc = DissipationCalculator()
    calc.load_commutators_from_skeleton()

    # Test operator loading
    assert len(calc.operators) == 20, f"Should load 20 operators, got {len(calc.operators)}"
    assert len(calc.commutators) == 400, f"Should load 400 commutators, got {len(calc.commutators)}"

    print(f"✓ Loaded {len(calc.operators)} operators")
    print(f"✓ Loaded {len(calc.commutators)} commutator pairs")

    # Test sequences with different operator classes
    test_sequences = {
        'A-Constructive': ['Kata', 'Seed', 'Weave', 'Latch'],  # All low λ
        'B-Disruptive': ['Ana', 'Non', 'Vale', 'Flux'],        # All high λ
        'C-Reflexive': ['Meta', 'Para', 'Echo', 'Crux'],       # All medium λ
        'Mixed': ['Ana', 'Kata', 'Meta', 'Telo', 'Echo'],      # Mix of all
    }

    print(f"\n✓ Testing dissipation analysis on 4 sequences:")
    for name, seq in test_sequences.items():
        analysis = calc.analyze_sequence(seq)
        print(f"    {name}: λ_eff={analysis['lambda_effective']:.3f}, half-life={analysis['half_life']:.2f}")

    # Verify λ matrix
    lambda_matrix = calc.get_lambda_matrix()
    assert lambda_matrix.shape == (20, 20), f"λ matrix should be 20×20, got {lambda_matrix.shape}"

    print(f"✓ λ matrix computed: {lambda_matrix.shape[0]}×{lambda_matrix.shape[1]}\n")


def test_phase_portrait():
    """Test phase portrait with all 20 operators"""
    print("="*70)
    print("TEST 4: Phase Portrait")
    print("="*70)

    portrait = PhasePortrait()

    # Test operator effects
    effects = portrait._default_operator_effects()
    assert len(effects) == 20, f"Should have 20 operator effects, got {len(effects)}"

    print(f"✓ Operator effects defined: {len(effects)} operators")

    # Test trajectories with new operators
    test_trajectories = {
        'Stabilize (new)': (['Seed', 'Latch', 'Axis'], (0.6, 0.6)),
        'Destabilize (new)': (['Vale', 'Flux', 'Fold'], (0.3, 0.3)),
        'Reflect (new)': (['Echo', 'Braid', 'Crux'], (0.5, 0.5)),
    }

    print(f"\n✓ Testing 3 trajectories:")
    for name, (seq, initial) in test_trajectories.items():
        traj = portrait.simulate_trajectory(initial, seq)
        final = traj[-1]
        print(f"    {name}: {traj[0]['attractor']} → {final['attractor']}")

    # Test basin structure
    basins = portrait.analyze_basin_structure(num_samples=500)
    print(f"\n✓ Basin structure (500 samples):")
    for att, size in basins['basin_sizes'].items():
        print(f"    {att}: {size:.1%}")
    print()


def test_inverse_solver():
    """Test inverse solver with all 20 operators"""
    print("="*70)
    print("TEST 5: Inverse Solver")
    print("="*70)

    solver = InverseSolver()
    solver.dissipation.load_commutators_from_skeleton()

    # Verify solver can access all operators
    assert len(solver.operators) == 20, f"Solver should have 20 operators, got {len(solver.operators)}"

    print(f"✓ Solver has access to {len(solver.operators)} operators")

    # Test solving with constraint to use new operators
    test_problems = [
        {
            'name': 'Gentle stabilization',
            'initial': (0.6, 0.6),
            'target': (0.2, 0.2),
        },
        {
            'name': 'Void escape',
            'initial': (0.9, 0.85),
            'target': (0.45, 0.45),
        },
    ]

    print(f"\n✓ Testing 2 inverse problems:")
    for prob in test_problems:
        solution = solver.solve(
            initial_state=prob['initial'],
            target_state=prob['target'],
            beam_width=10,
            verbose=False
        )

        # Check if solution uses any new operators
        new_ops = {'Echo', 'Braid', 'Fold', 'Seed', 'Crux', 'Weave', 'Bind', 'Axis', 'Vale', 'Flux', 'Latch'}
        uses_new = any(op in new_ops for op in solution['sequence'])

        status = "✓" if solution['success'] else "⚠"
        new_marker = "[NEW]" if uses_new else ""
        print(f"    {status} {prob['name']}: {' ∘ '.join(solution['sequence'])} {new_marker}")

    print()


def test_cli_integration():
    """Test CLI with all 20 operators"""
    print("="*70)
    print("TEST 6: CLI Integration")
    print("="*70)

    compiler = ControlledRuptureCompiler()

    # Verify commutators loaded
    assert len(compiler.dissipation.commutators) == 400, "CLI should load 400 commutators"

    print(f"✓ CLI loaded {len(compiler.dissipation.commutators)} commutator pairs")

    # Test analyze with new operators
    new_op_sequence = ['Seed', 'Weave', 'Bind', 'Latch']
    analysis = compiler.dissipation.analyze_sequence(new_op_sequence)

    print(f"✓ Analyzed sequence: {' ∘ '.join(new_op_sequence)}")
    print(f"    λ_eff={analysis['lambda_effective']:.3f}, half-life={analysis['half_life']:.2f}")

    # Test diagnose
    problem_keys = list(compiler.problem_templates.keys())
    print(f"\n✓ Available problem templates: {len(problem_keys)}")
    for key in problem_keys:
        print(f"    - {key}")

    print()


def test_operator_classes():
    """Verify operator classifications are consistent"""
    print("="*70)
    print("TEST 7: Operator Classifications")
    print("="*70)

    formalism_path = Path(__file__).parent / "formalism.json"
    with open(formalism_path) as f:
        formalism = json.load(f)

    # Group operators by class
    by_class = {
        'A-Constructive': [],
        'B-Disruptive': [],
        'C-Reflexive': [],
        'D-Structural': [],
    }

    for name, data in formalism['operators'].items():
        op_class = data['class']
        lambda_val = data['lambda_intrinsic']
        by_class[op_class].append((name, lambda_val))

    # Print classifications
    for cls, ops in sorted(by_class.items()):
        print(f"\n{cls} ({len(ops)} operators):")
        for name, lambda_val in sorted(ops, key=lambda x: x[1]):
            print(f"    {name:8s} λ={lambda_val:.2f}")

    # Verify A-Constructive has low λ, B-Disruptive has high λ
    constructive_lambdas = [lam for _, lam in by_class['A-Constructive']]
    disruptive_lambdas = [lam for _, lam in by_class['B-Disruptive']]

    avg_constructive = sum(constructive_lambdas) / len(constructive_lambdas)
    avg_disruptive = sum(disruptive_lambdas) / len(disruptive_lambdas)

    assert avg_constructive < avg_disruptive, "Constructive ops should have lower average λ than disruptive"

    print(f"\n✓ Average λ by class:")
    print(f"    A-Constructive: {avg_constructive:.3f}")
    print(f"    B-Disruptive: {avg_disruptive:.3f}")
    print(f"    Verification: Constructive < Disruptive ✓\n")


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("COMPREHENSIVE 20-OPERATOR TEST SUITE")
    print("Controlled Rupture Compiler v2.0.0")
    print("="*70 + "\n")

    tests = [
        test_formalism_structure,
        test_commutator_skeleton,
        test_dissipation_calculator,
        test_phase_portrait,
        test_inverse_solver,
        test_cli_integration,
        test_operator_classes,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ FAILED: {e}\n")
            failed += 1
        except Exception as e:
            print(f"✗ ERROR: {e}\n")
            failed += 1

    # Summary
    print("="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")

    if failed == 0:
        print("\n✓ ALL TESTS PASSED - 20-OPERATOR SYSTEM FULLY OPERATIONAL\n")
    else:
        print(f"\n⚠ {failed} test(s) failed\n")

    return failed == 0


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
