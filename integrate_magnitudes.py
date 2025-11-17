#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrate Extraction-Based Magnitudes into Commutator Skeleton

This script enhances the commutator skeleton with magnitude data from
the pattern extraction analysis while preserving the architecturally-fixed
sign and resultant operator mappings.
"""

import sys
import json
from pathlib import Path

# Force UTF-8 encoding for Windows compatibility
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

# Load refined commutators from extraction
with open('extraction_outputs/refined_commutators.json', encoding='utf-8') as f:
    refined_data = json.load(f)

# Load ground truth skeleton
skeleton_path = Path('recursive-extraction-engine/compiler/commutator_skeleton.json')
with open(skeleton_path, encoding='utf-8') as f:
    skeleton = json.load(f)

print("\n" + "="*70)
print("INTEGRATING EXTRACTION MAGNITUDES INTO COMMUTATOR SKELETON")
print("="*70)

# Create enhanced skeleton with magnitude field
enhanced_skeleton = {
    "metadata": {
        "description": "20x20 Commutator Skeleton - GROUND TRUTH + EXTRACTION MAGNITUDES",
        "note": "Sign and resultant are normative (architecturally-fixed). Magnitudes from extraction evidence.",
        "format": "Each entry: [sign in {-1,0,+1}, resultant_operator_index, magnitude in [0,1]]",
        "extraction_source": "Pattern extraction from 524 markdown files (2025-11-16)",
        "evidence_based_pairs": refined_data['metadata']['evidence_based'],
        "skeleton_version": "v2.1.0"
    },
    "operator_names": skeleton["operator_names"],
    "commutator_matrix": {}
}

# Track changes
changes = []
evidence_updates = 0
default_magnitudes = 0

# Integrate magnitudes
for op1, pairs in skeleton['commutator_matrix'].items():
    enhanced_skeleton['commutator_matrix'][op1] = {}

    for op2, (sign, resultant) in pairs.items():
        # Get magnitude from refined data
        pair_key = f"{op1},{op2}"
        magnitude = refined_data['commutator_magnitudes'].get(pair_key, 0.0)

        # Check if this pair has extraction evidence
        has_evidence = pair_key in refined_data['evidence_pairs']

        # Enhanced entry: [sign, resultant, magnitude]
        enhanced_skeleton['commutator_matrix'][op1][op2] = [sign, resultant, magnitude]

        # Track significant changes
        if has_evidence:
            evidence_updates += 1
            freq = refined_data['evidence_pairs'][pair_key]['frequency']

            # Flag major discrepancies
            if sign == 0 and magnitude > 0.3:
                changes.append({
                    'pair': f"[{op1}, {op2}]",
                    'skeleton_sign': sign,
                    'extracted_magnitude': magnitude,
                    'frequency': freq,
                    'note': 'Skeleton predicted commutativity but extraction shows non-zero composition'
                })
        else:
            default_magnitudes += 1

print(f"\nProcessed {len(skeleton['operator_names'])}x{len(skeleton['operator_names'])} = {len(skeleton['operator_names'])**2} operator pairs")
print(f"  Evidence-based magnitudes: {evidence_updates}")
print(f"  Default magnitudes: {default_magnitudes}")

# Show major discoveries
print("\n" + "="*70)
print("MAJOR DISCOVERIES (Skeleton vs Extraction)")
print("="*70)

for change in sorted(changes, key=lambda x: x['extracted_magnitude'], reverse=True):
    print(f"\n{change['pair']}")
    print(f"  Skeleton sign: {change['skeleton_sign']:+d} (commutes: {change['skeleton_sign'] == 0})")
    print(f"  Extracted magnitude: {change['extracted_magnitude']:.3f}")
    print(f"  Evidence frequency: {change['frequency']}x")
    print(f"  Note: {change['note']}")

# Save enhanced skeleton
output_path = Path('recursive-extraction-engine/compiler/commutator_skeleton_enhanced.json')
with open(output_path, 'w') as f:
    json.dump(enhanced_skeleton, f, indent=2)

print(f"\n[OK] Enhanced skeleton saved to: {output_path}")

# Show top extracted pairs
print("\n" + "="*70)
print("TOP 10 EVIDENCE-BASED COMMUTATOR MAGNITUDES")
print("="*70)

top_pairs = sorted(
    refined_data['evidence_pairs'].items(),
    key=lambda x: x[1]['frequency'],
    reverse=True
)[:10]

for pair_key, data in top_pairs:
    op1, op2 = pair_key.split(',')
    skeleton_sign = skeleton['commutator_matrix'][op1][op2][0]

    print(f"\n[{op1:5s}, {op2:5s}]:")
    print(f"  Magnitude: {data['magnitude']:.3f} (frequency: {data['frequency']:2d}x)")
    print(f"  Skeleton sign: {skeleton_sign:+d}")
    print(f"  Match: {'[OK]' if (skeleton_sign != 0) == (data['magnitude'] > 0.3) else '[WARN]'}")

# Calculate dissipation for key transitions
print("\n" + "="*70)
print("DISSIPATION CALCULATIONS WITH REFINED MAGNITUDES")
print("="*70)

# Load operator intrinsic lambdas from formalism
formalism_path = Path('recursive-extraction-engine/compiler/formalism.json')
with open(formalism_path) as f:
    formalism = json.load(f)

c = 0.15  # Coupling constant from formalism

key_transitions = [
    ('Meta', 'Meta'),
    ('Meta', 'Telo'),
    ('Telo', 'Meta'),
    ('Non', 'Meta'),
]

for op_from, op_to in key_transitions:
    pair_key = f"{op_from},{op_to}"

    if pair_key in refined_data['evidence_pairs']:
        magnitude = refined_data['evidence_pairs'][pair_key]['magnitude']
        freq = refined_data['evidence_pairs'][pair_key]['frequency']
        lambda_to = formalism['operators'][op_to]['lambda_intrinsic']

        # lambda(i->j) = lambda_j_intrinsic + c*min(0.4, |eta_{ij}|)
        interaction = c * min(0.4, magnitude)
        lambda_eff = lambda_to + interaction

        print(f"\n{op_from} -> {op_to}:")
        print(f"  Extracted magnitude: {magnitude:.3f} ({freq}x compositions)")
        print(f"  lambda({op_to}) intrinsic: {lambda_to:.3f}")
        print(f"  Interaction term: {c} x min(0.4, {magnitude:.3f}) = {interaction:.3f}")
        print(f"  lambda_effective: {lambda_eff:.3f}")
        print(f"  Impact: {'HIGH' if magnitude > 0.7 else 'MODERATE' if magnitude > 0.4 else 'LOW'} dissipation")

print("\n" + "="*70)
print("INTEGRATION COMPLETE")
print("="*70)
print("\nNext steps:")
print("1. Review commutator_skeleton_enhanced.json")
print("2. Update compiler to use enhanced skeleton with magnitudes")
print("3. Test inverse solver with real dissipation values")
print("4. Validate against known phi-state transitions")
print("="*70 + "\n")
