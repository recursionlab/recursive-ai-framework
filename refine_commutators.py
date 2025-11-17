# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Commutator Magnitude Refinement
Uses composition frequency data to refine commutator magnitudes from default 1.0
"""

import sys
# Force UTF-8 encoding for Windows compatibility
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

import json
from pathlib import Path
from collections import Counter

# Load operator mapping
with open('extraction_outputs/operator_mapping.json', encoding='utf-8') as f:
    mapping_data = json.load(f)

primary_mappings = mapping_data['primary_recommendations']

# Load pattern extraction to get composition frequencies
with open('extraction_outputs/pattern_extraction.json', encoding='utf-8') as f:
    extraction_data = json.load(f)

# Aggregate composition frequencies
symbolic_compositions = Counter()
for entry in extraction_data:
    for comp in entry['compositions']:
        symbolic_compositions[comp] += 1

print("\n" + "="*70)
print("COMMUTATOR MAGNITUDE REFINEMENT")
print("="*70)

# Convert symbolic compositions to normative using mapping
normative_compositions = Counter()
unmapped_comps = []

for comp, freq in symbolic_compositions.items():
    # Parse composition "Op1 ∘ Op2"
    parts = comp.split(' ∘ ')
    if len(parts) == 2:
        op1_sym, op2_sym = parts

        # Map to normative
        op1_norm = primary_mappings.get(op1_sym)
        op2_norm = primary_mappings.get(op2_sym)

        if op1_norm and op2_norm:
            norm_comp = f"{op1_norm} ∘ {op2_norm}"
            normative_compositions[norm_comp] += freq
        else:
            unmapped_comps.append(comp)

print(f"\nSymbolic compositions found: {len(symbolic_compositions)}")
print(f"Mapped to normative: {len(normative_compositions)}")
print(f"Unmapped (need secondary mappings): {len(unmapped_comps)}")

# Calculate commutator magnitudes
# Formula: magnitude ∝ frequency^0.5 (square root to prevent over-weighting high frequencies)
# Normalize to [0, 1] range

max_freq = max(normative_compositions.values()) if normative_compositions else 1

commutator_magnitudes = {}
for comp, freq in normative_compositions.items():
    parts = comp.split(' ∘ ')
    if len(parts) == 2:
        op1, op2 = parts

        # Calculate magnitude estimate
        # Use sqrt to dampen effect of very high frequencies
        raw_magnitude = (freq / max_freq) ** 0.5

        # Scale to reasonable range [0.2, 1.0]
        # Even infrequent compositions should have some magnitude
        magnitude = 0.2 + (raw_magnitude * 0.8)

        commutator_magnitudes[(op1, op2)] = {
            'magnitude': round(magnitude, 3),
            'frequency': freq,
            'evidence': 'extracted'
        }

print("\n" + "="*70)
print("REFINED COMMUTATOR MAGNITUDES")
print("="*70)
print("\nTop 15 non-commutative pairs (by frequency):")

sorted_comms = sorted(commutator_magnitudes.items(),
                     key=lambda x: x[1]['frequency'],
                     reverse=True)

for (op1, op2), data in sorted_comms[:15]:
    print(f"  [{op1:5s}, {op2:5s}]: magnitude={data['magnitude']:.3f} (freq={data['frequency']:2d}x)")

# Load current commutator skeleton for comparison
formalism_path = Path('recursive-extraction-engine/compiler/commutator_skeleton.json')
with open(formalism_path) as f:
    skeleton = json.load(f)

# Compare with ground truth skeleton
print("\n" + "="*70)
print("COMPARISON WITH GROUND TRUTH SKELETON")
print("="*70)

matches = 0
mismatches = 0

for (op1, op2), data in commutator_magnitudes.items():
    if op1 in skeleton['commutator_matrix'] and op2 in skeleton['commutator_matrix'][op1]:
        sign, _ = skeleton['commutator_matrix'][op1][op2]

        if sign != 0:  # Non-zero commutator expected
            matches += 1
            print(f"  ✓ [{op1}, {op2}]: Skeleton sign={sign:+d}, Extracted mag={data['magnitude']:.3f}")
        else:  # Zero commutator expected but we found composition
            mismatches += 1
            print(f"  ⚠ [{op1}, {op2}]: Skeleton says zero but extracted {data['frequency']}x compositions")

print(f"\nMatches with skeleton: {matches}")
print(f"Potential refinements: {mismatches}")

# Generate updated commutator values
print("\n" + "="*70)
print("RECOMMENDED UPDATES TO COMMUTATOR MATRIX")
print("="*70)

# Start with skeleton defaults (sign-based: 0 or 1.0)
# Then update with extracted evidence

updated_commutators = {}

# First pass: Load skeleton defaults
for op1, pairs in skeleton['commutator_matrix'].items():
    for op2, (sign, _) in pairs.items():
        if sign != 0:
            updated_commutators[(op1, op2)] = 1.0  # Default for non-zero
        else:
            updated_commutators[(op1, op2)] = 0.0  # Neutral

# Second pass: Update with extracted evidence
for (op1, op2), data in commutator_magnitudes.items():
    updated_commutators[(op1, op2)] = data['magnitude']

# Compute statistics
total_pairs = len(updated_commutators)
evidence_based = len(commutator_magnitudes)
default_based = total_pairs - evidence_based

print(f"\nTotal operator pairs: {total_pairs}")
print(f"  Refined from extraction: {evidence_based} ({evidence_based/total_pairs:.1%})")
print(f"  Using skeleton defaults: {default_based} ({default_based/total_pairs:.1%})")

# Show specific refined values for key pairs
print("\nKey refined commutator magnitudes:")
key_pairs = [
    ('Meta', 'Meta'),
    ('Meta', 'Telo'),
    ('Meta', 'Para'),
    ('Ana', 'Non'),
    ('Telo', 'Pro'),
]

for op1, op2 in key_pairs:
    if (op1, op2) in updated_commutators:
        mag = updated_commutators[(op1, op2)]
        source = "extracted" if (op1, op2) in commutator_magnitudes else "skeleton"
        print(f"  [{op1:5s}, {op2:5s}]: {mag:.3f} ({source})")

# Save refined commutators
output = {
    'metadata': {
        'source': 'Pattern extraction + Ground truth skeleton',
        'total_pairs': total_pairs,
        'evidence_based': evidence_based,
        'default_based': default_based,
        'extraction_files': 524
    },
    'commutator_magnitudes': {
        f"{op1},{op2}": mag
        for (op1, op2), mag in updated_commutators.items()
    },
    'evidence_pairs': {
        f"{op1},{op2}": data
        for (op1, op2), data in commutator_magnitudes.items()
    },
    'composition_frequencies': {
        comp: freq
        for comp, freq in normative_compositions.most_common()
    }
}

output_file = Path('extraction_outputs/refined_commutators.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print(f"\n✓ Refined commutators saved to: {output_file}")

# Calculate impact on dissipation calculations
print("\n" + "="*70)
print("IMPACT ON DISSIPATION CALCULATIONS")
print("="*70)

# Example: Meta ∘ Meta (most common composition in extracted data)
if ('Meta', 'Meta') in commutator_magnitudes:
    data = commutator_magnitudes[('Meta', 'Meta')]

    # λ(i→j) = λ_j_intrinsic + c·min(0.4, |η_{ij}|)
    lambda_meta = 0.80  # From formalism
    c = 0.15
    interaction = c * min(0.4, data['magnitude'])
    lambda_effective = lambda_meta + interaction

    print(f"\nMeta ∘ Meta composition:")
    print(f"  Extracted frequency: {data['frequency']}x")
    print(f"  Refined magnitude: {data['magnitude']:.3f}")
    print(f"  λ(Meta→Meta) = {lambda_meta} + {c} × {min(0.4, data['magnitude']):.3f} = {lambda_effective:.3f}")
    print(f"  Impact: {'High' if data['magnitude'] > 0.7 else 'Moderate' if data['magnitude'] > 0.4 else 'Low'} dissipation")

print("="*70 + "\n")
