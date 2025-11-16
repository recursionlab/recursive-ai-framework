#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Torsion Field Computation Engine

Implements the canonical reduction:
    C(x) → ∇C → T = antiSym(∇C) → T=0 ⟺ Invariance

Maps 73,949 contradictions to torsion field on epistemic manifold.
"""

import sys

# Force UTF-8 encoding for Windows compatibility
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

import json
import numpy as np
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

print("\n" + "="*70)
print("TORSION FIELD COMPUTATION ENGINE")
print("Contradiction → Invariance via Differential Geometry")
print("="*70)

# ==============================================================================
# STEP 1: BUILD CONTRADICTION VECTOR FIELD C(x): M → TM
# ==============================================================================

print("\n" + "─"*70)
print("STEP 1: Building Contradiction Vector Field C(x)")
print("─"*70)

# Load extraction data
with open('extraction_outputs/pattern_extraction.json') as f:
    extraction_data = json.load(f)

# Load operator mappings
with open('extraction_outputs/operator_mapping.json') as f:
    operator_mapping = json.load(f)

# Load commutator magnitudes
with open('extraction_outputs/refined_commutators.json') as f:
    commutator_data = json.load(f)

print(f"\n✓ Loaded {len(extraction_data)} files")

# Build C(x): M → TM
# x = (operator_pair, file, context_type)
# C(x) = tangent vector showing how meaning "wants to break"

contradiction_field = {}
field_statistics = defaultdict(int)

total_contradictions = 0

for entry in extraction_data:
    file_name = Path(entry['file']).name

    for contradiction in entry['contradictions']:
        keyword = contradiction['keyword']
        context = contradiction['context']

        # Extract operator mentions in context
        operators_in_context = []
        for symbol, mapping_data in operator_mapping['mappings'].items():
            if symbol in context:
                # Take primary recommendation
                primary_op = mapping_data['likely_normative'][0]
                operators_in_context.append(primary_op)

        # Determine operator pair (if identifiable)
        operator_pair = None
        if len(operators_in_context) >= 2:
            operator_pair = tuple(operators_in_context[:2])
        elif len(operators_in_context) == 1:
            # Self-interaction
            operator_pair = (operators_in_context[0], operators_in_context[0])

        # Semantic location x
        x = (operator_pair, file_name, keyword)

        # Tangent vector C(x)
        if x not in contradiction_field:
            contradiction_field[x] = {
                'count': 0,
                'contexts': [],
                'operator_pair': operator_pair,
                'file': file_name,
                'type': keyword
            }

        contradiction_field[x]['count'] += 1
        contradiction_field[x]['contexts'].append(context[:200])

        field_statistics[keyword] += 1
        total_contradictions += 1

print(f"\n✓ Built contradiction field C(x): M → TM")
print(f"  Total contradictions: {total_contradictions:,}")
print(f"  Unique locations |M|: {len(contradiction_field):,}")
print(f"\nField statistics by type:")
for ctype, count in sorted(field_statistics.items(), key=lambda x: x[1], reverse=True):
    print(f"  {ctype:15s}: {count:6,} ({count/total_contradictions*100:4.1f}%)")

# ==============================================================================
# STEP 2: COMPUTE GRADIENT ∇C (Directional Curvature)
# ==============================================================================

print("\n" + "─"*70)
print("STEP 2: Computing Gradient ∇C")
print("─"*70)

gradient_field = {}

# For each location x, compute partial derivatives
for x, C_x in contradiction_field.items():
    operator_pair, file_name, ctype = x

    # ∂C/∂operator (how C changes with operator variation)
    # Approximate by comparing to nearby operator pairs
    partial_operator = 0.0
    if operator_pair is not None and len(operator_pair) == 2:
        op1, op2 = operator_pair
        pair_key = f"{op1},{op2}"

        # Use commutator magnitude as directional derivative strength
        if pair_key in commutator_data['commutator_magnitudes']:
            partial_operator = commutator_data['commutator_magnitudes'][pair_key]

    # ∂C/∂context (how C changes with context type)
    # Approximate by comparing contradiction counts across types
    partial_context = C_x['count'] / total_contradictions

    # Full gradient vector
    gradient_field[x] = {
        'partial_operator': partial_operator,
        'partial_context': partial_context,
        'magnitude': np.sqrt(partial_operator**2 + partial_context**2),
        'direction': (partial_operator, partial_context)
    }

print(f"\n✓ Computed gradient field ∇C")
print(f"  Locations with gradient: {len(gradient_field):,}")

# Statistics
gradients = [g['magnitude'] for g in gradient_field.values()]
print(f"\nGradient statistics:")
print(f"  Mean |∇C|: {np.mean(gradients):.4f}")
print(f"  Max |∇C|:  {np.max(gradients):.4f}")
print(f"  Min |∇C|:  {np.min(gradients):.4f}")

# ==============================================================================
# STEP 3: COMPUTE TORSION T = antiSym(∇C)
# ==============================================================================

print("\n" + "─"*70)
print("STEP 3: Computing Torsion T = antiSym(∇C)")
print("─"*70)

torsion_field = {}

# Group by operator pairs to compute antisymmetric part
operator_pair_groups = defaultdict(list)

for x, grad in gradient_field.items():
    operator_pair = x[0]
    if operator_pair is not None and len(operator_pair) == 2:
        # Normalize pair ordering for antisymmetrization
        op1, op2 = operator_pair
        canonical_pair = tuple(sorted([op1, op2]))
        operator_pair_groups[canonical_pair].append((x, grad))

# Compute torsion for each operator pair
for canonical_pair, locations in operator_pair_groups.items():
    op1, op2 = canonical_pair

    # Find forward and reverse directions
    forward_grad = None
    reverse_grad = None

    for x, grad in locations:
        actual_pair = x[0]
        if actual_pair == (op1, op2):
            forward_grad = grad
        elif actual_pair == (op2, op1):
            reverse_grad = grad

    # Antisymmetric part: T = ∂_μ C_ν - ∂_ν C_μ
    if forward_grad and reverse_grad:
        # Full antisymmetrization
        T_value = forward_grad['partial_operator'] - reverse_grad['partial_operator']
    elif forward_grad:
        # Only forward direction exists
        T_value = forward_grad['partial_operator']
    elif reverse_grad:
        # Only reverse direction exists
        T_value = -reverse_grad['partial_operator']
    else:
        T_value = 0.0

    # Store torsion
    torsion_field[canonical_pair] = {
        'torsion': T_value,
        'abs_torsion': abs(T_value),
        'op1': op1,
        'op2': op2,
        'locations_count': len(locations)
    }

print(f"\n✓ Computed torsion field T")
print(f"  Operator pairs with torsion: {len(torsion_field)}")

# Statistics
torsions = [t['abs_torsion'] for t in torsion_field.values()]
print(f"\nTorsion statistics:")
print(f"  Mean |T|: {np.mean(torsions):.4f}")
print(f"  Max |T|:  {np.max(torsions):.4f}")
print(f"  Min |T|:  {np.min(torsions):.4f}")

# Top torsion pairs
print(f"\nTop 10 torsion pairs (highest curvature):")
sorted_torsion = sorted(torsion_field.items(), key=lambda x: x[1]['abs_torsion'], reverse=True)
for (pair, data) in sorted_torsion[:10]:
    print(f"  [{data['op1']:5s}, {data['op2']:5s}]: T = {data['torsion']:+.4f} (|T| = {data['abs_torsion']:.4f})")

# ==============================================================================
# STEP 4: FIND INVARIANTS (T = 0 Regions)
# ==============================================================================

print("\n" + "─"*70)
print("STEP 4: Finding Invariants (T ≈ 0)")
print("─"*70)

# Tolerance for "near-zero" torsion
epsilon = 0.01

invariants = []

for pair, data in torsion_field.items():
    if data['abs_torsion'] < epsilon:
        invariants.append({
            'pair': pair,
            'op1': data['op1'],
            'op2': data['op2'],
            'torsion': data['torsion'],
            'abs_torsion': data['abs_torsion'],
            'locations': data['locations_count']
        })

print(f"\n✓ Found {len(invariants)} invariant regions (|T| < {epsilon})")

if len(invariants) > 0:
    print(f"\nInvariant operator pairs:")
    for inv in sorted(invariants, key=lambda x: x['abs_torsion'])[:20]:
        print(f"  [{inv['op1']:5s}, {inv['op2']:5s}]: T = {inv['torsion']:+.6f}")
else:
    print("\n⚠ No exact invariants found at ε = {epsilon}")
    print("  Increasing tolerance...")

    epsilon = 0.1
    for pair, data in torsion_field.items():
        if data['abs_torsion'] < epsilon:
            invariants.append({
                'pair': pair,
                'op1': data['op1'],
                'op2': data['op2'],
                'torsion': data['torsion'],
                'abs_torsion': data['abs_torsion'],
                'locations': data['locations_count']
            })

    print(f"\n✓ Found {len(invariants)} near-invariants (|T| < {epsilon})")

# ==============================================================================
# STEP 5: MAP TO ATTRACTORS (J=0, S*, ∅)
# ==============================================================================

print("\n" + "─"*70)
print("STEP 5: Mapping Invariants to Attractors")
print("─"*70)

# Load operator intrinsic dissipation values
with open('recursive-extraction-engine/compiler/formalism.json') as f:
    formalism = json.load(f)

attractor_map = {
    'J=0': [],  # Low dissipation, low contradiction
    'S*': [],   # Moderate dissipation, productive contradiction
    '∅': []     # High dissipation, collapse
}

for inv in invariants:
    op1, op2 = inv['op1'], inv['op2']

    # Estimate J' level based on operator dissipation
    lambda1 = formalism['operators'].get(op1, {}).get('lambda_intrinsic', 0.5)
    lambda2 = formalism['operators'].get(op2, {}).get('lambda_intrinsic', 0.5)

    # Average dissipation as J' proxy
    avg_lambda = (lambda1 + lambda2) / 2

    # Map to attractors
    if avg_lambda < 0.35:
        attractor = 'J=0'
    elif avg_lambda < 0.70:
        attractor = 'S*'
    else:
        attractor = '∅'

    inv['attractor'] = attractor
    inv['J_prime_estimate'] = avg_lambda
    attractor_map[attractor].append(inv)

print(f"\n✓ Mapped {len(invariants)} invariants to attractors")
print(f"\nAttractor distribution:")
for attractor, invs in attractor_map.items():
    count = len(invs)
    pct = count / len(invariants) * 100 if len(invariants) > 0 else 0
    print(f"  {attractor:5s}: {count:3d} invariants ({pct:4.1f}%)")

# Show examples from each attractor
print(f"\nExample invariants by attractor:")
for attractor in ['J=0', 'S*', '∅']:
    invs = attractor_map[attractor]
    if len(invs) > 0:
        print(f"\n  {attractor} (J' ≈ {invs[0]['J_prime_estimate']:.2f}):")
        for inv in invs[:3]:
            print(f"    [{inv['op1']:5s}, {inv['op2']:5s}]: T = {inv['torsion']:+.6f}, λ̄ = {inv['J_prime_estimate']:.3f}")

# ==============================================================================
# SAVE RESULTS
# ==============================================================================

print("\n" + "─"*70)
print("SAVING RESULTS")
print("─"*70)

output = {
    'metadata': {
        'description': 'Torsion field analysis: Contradiction → Invariance',
        'total_contradictions': total_contradictions,
        'unique_locations': len(contradiction_field),
        'torsion_pairs': len(torsion_field),
        'invariants': len(invariants),
        'epsilon': epsilon,
        'date': '2025-11-16'
    },
    'field_statistics': dict(field_statistics),
    'gradient_statistics': {
        'mean': float(np.mean(gradients)),
        'max': float(np.max(gradients)),
        'min': float(np.min(gradients)),
        'std': float(np.std(gradients))
    },
    'torsion_statistics': {
        'mean': float(np.mean(torsions)),
        'max': float(np.max(torsions)),
        'min': float(np.min(torsions)),
        'std': float(np.std(torsions))
    },
    'torsion_field': {
        str(pair): {
            'op1': data['op1'],
            'op2': data['op2'],
            'torsion': float(data['torsion']),
            'abs_torsion': float(data['abs_torsion']),
            'locations': data['locations_count']
        }
        for pair, data in torsion_field.items()
    },
    'invariants': [
        {
            'op1': inv['op1'],
            'op2': inv['op2'],
            'torsion': float(inv['torsion']),
            'abs_torsion': float(inv['abs_torsion']),
            'attractor': inv['attractor'],
            'J_prime_estimate': float(inv['J_prime_estimate']),
            'locations': inv['locations']
        }
        for inv in invariants
    ],
    'attractor_distribution': {
        attractor: len(invs)
        for attractor, invs in attractor_map.items()
    }
}

output_path = Path('extraction_outputs/torsion_field_analysis.json')
with open(output_path, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n✓ Saved to: {output_path}")

# ==============================================================================
# SUMMARY
# ==============================================================================

print("\n" + "="*70)
print("TORSION FIELD ANALYSIS COMPLETE")
print("="*70)

print(f"""
Master Equation Implementation:
  C(x) → ∇C → T = antiSym(∇C) → T=0 ⟺ Invariance

Results:
  • Contradiction field C(x): {len(contradiction_field):,} locations
  • Gradient field ∇C computed
  • Torsion field T: {len(torsion_field)} operator pairs
  • Invariants (T≈0): {len(invariants)} pairs

Attractor Mapping:
  • J=0 (low contradiction): {len(attractor_map['J=0'])} invariants
  • S* (productive): {len(attractor_map['S*'])} invariants
  • ∅ (collapse): {len(attractor_map['∅'])} invariants

Key Finding:
  Contradiction becomes invariance when antisymmetric curvature vanishes.
  T = 0 defines stable semantic regions (attractors).
""")

print("="*70 + "\n")
