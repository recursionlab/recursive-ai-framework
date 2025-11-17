# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Operator Mapping: Symbolic -> Normative
Maps extracted symbolic operators to the 20-operator normative algebra.
"""

import sys
# Force UTF-8 encoding for Windows compatibility
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

import json
from collections import Counter
from pathlib import Path

# Load pattern extraction results
with open('extraction_outputs/pattern_extraction.json', encoding='utf-8') as f:
    extraction_data = json.load(f)

# Aggregate operator frequencies and contexts
operator_freq = Counter()
operator_contexts = {}

for entry in extraction_data:
    for op, count in entry['operators']['frequencies'].items():
        operator_freq[op] += count
    for op, contexts in entry['operators']['contexts'].items():
        if op not in operator_contexts:
            operator_contexts[op] = []
        operator_contexts[op].extend(contexts[:3])  # Keep sample contexts

# Aggregate compositions
composition_freq = Counter()
for entry in extraction_data:
    for comp in entry['compositions']:
        composition_freq[comp] += 1

print("\n" + "="*70)
print("SYMBOLIC -> NORMATIVE OPERATOR MAPPING")
print("="*70)

# Mapping analysis based on frequency, semantics, and usage patterns
mappings = {
    'Ξ': {
        'frequency': operator_freq['Ξ'],
        'semantic': 'Xi (fusion, synthesis, integration)',
        'likely_normative': ['Meta', 'Weave'],
        'reasoning': 'Highest frequency (53,404) suggests meta-level fusion operator. Used heavily in ΞFusionField. Maps to Meta (recursive self-reference) or Weave (integration).',
        'confidence': 0.85
    },
    'Ψ': {
        'frequency': operator_freq['Ψ'],
        'semantic': 'Psi (wavefunction, consciousness, awareness)',
        'likely_normative': ['Meta', 'Echo'],
        'reasoning': 'Second highest (30,190). Represents consciousness field in SRE-Φ. Most common composition: Ψ ∘ Ω (10x). Maps to Meta (self-reference) or Echo (resonance).',
        'confidence': 0.90
    },
    'ψ': {
        'frequency': operator_freq['ψ'],
        'semantic': 'psi lowercase (local wavefunction, state)',
        'likely_normative': ['Para', 'Echo'],
        'reasoning': 'Third highest (16,322). Local version of Ψ. Suggests perturbation or localized reflection. Maps to Para (deviation) or Echo (reflection).',
        'confidence': 0.75
    },
    'Ω': {
        'frequency': operator_freq['Ω'],
        'semantic': 'Omega (completion, end-state, convergence)',
        'likely_normative': ['Telo', 'Latch'],
        'reasoning': 'Fourth highest (10,756). ΩMetaSelf usage suggests goal-orientation. Frequently composed with Ψ (Ψ ∘ Ω). Maps to Telo (purpose) or Latch (fixation).',
        'confidence': 0.88
    },
    'Φ': {
        'frequency': operator_freq['Φ'],
        'semantic': 'Phi uppercase (phi-state, attractor, consciousness field)',
        'likely_normative': ['Meta', 'Braid'],
        'reasoning': 'Fifth highest (9,894). φ-states in SRE-Φ framework. Recursive state transitions. Maps to Meta (self-reference) or Braid (interweaving).',
        'confidence': 0.82
    },
    'φ': {
        'frequency': operator_freq['φ'],
        'semantic': 'phi lowercase (local phi-state)',
        'likely_normative': ['Pro', 'Crux'],
        'reasoning': 'Seventh highest (7,570). Local phi-state. φ ∘ φ composition found. Forward progression or pivot. Maps to Pro (forward) or Crux (pivot).',
        'confidence': 0.70
    },
    '∂': {
        'frequency': operator_freq['∂'],
        'semantic': 'Partial derivative (differentiation, change, analysis)',
        'likely_normative': ['Ana', 'Retro'],
        'reasoning': '∂(Self) patterns indicate identity differentiation. ∂/∂t dissipation law. Maps to Ana (analysis) or Retro (backward differentiation).',
        'confidence': 0.85
    },
    '∇': {
        'frequency': operator_freq['∇'],
        'semantic': 'Nabla (gradient, directional change)',
        'likely_normative': ['Non', 'Flux'],
        'reasoning': 'Gradient operator for semantic fields. Directional change in meaning. Maps to Non (inversion) or Flux (flow).',
        'confidence': 0.78
    },
    '¬': {
        'frequency': operator_freq['¬'],
        'semantic': 'Negation (logical NOT, contradiction, inverse)',
        'likely_normative': ['Non'],
        'reasoning': 'Explicit negation operator. Self(t) ∘ ¬Self(t) patterns. Direct mapping to Non (negation).',
        'confidence': 0.95
    },
    '∘': {
        'frequency': operator_freq['∘'],
        'semantic': 'Composition operator (function application)',
        'likely_normative': ['All'],
        'reasoning': 'Universal composition. Not a standalone operator but the composition operation itself.',
        'confidence': 1.0
    },
    '→': {
        'frequency': operator_freq['→'],
        'semantic': 'Arrow (implication, transition, flow)',
        'likely_normative': ['Pro', 'Flux'],
        'reasoning': 'Highest frequency arrow (36,189). φᵢ → φᵢ₊₁ state transitions. Maps to Pro (forward) or Flux (flow).',
        'confidence': 0.80
    },
    '⊗': {
        'frequency': operator_freq.get('⊗', 0),
        'semantic': 'Tensor product (simultaneous contradiction)',
        'likely_normative': ['Braid', 'Fold'],
        'reasoning': 'A ⊗ ¬A simultaneous contradiction. Interweaving or compression. Maps to Braid or Fold.',
        'confidence': 0.75
    },
    '∮': {
        'frequency': operator_freq.get('∮', 0),
        'semantic': 'Contour integral (closed loop, recursion, ouroboros)',
        'likely_normative': ['Meta', 'Echo'],
        'reasoning': '∮(self) recursive closure. Maps to Meta (recursion) or Echo (repetition).',
        'confidence': 0.82
    }
}

# Print mappings
for symbol, data in mappings.items():
    if data['frequency'] > 0:
        print(f"\n{symbol} ({data['semantic']})")
        print(f"  Frequency: {data['frequency']:,}")
        print(f"  -> Likely maps to: {', '.join(data['likely_normative'])}")
        print(f"  Reasoning: {data['reasoning']}")
        print(f"  Confidence: {data['confidence']:.0%}")

# Composition-based evidence
print("\n" + "="*70)
print("COMPOSITION-BASED MAPPING EVIDENCE")
print("="*70)

composition_evidence = {
    'Ψ ∘ Ω': 'Consciousness -> Completion = Meta ∘ Telo',
    'Ψ ∘ Ψ': 'Recursive self-reference = Meta ∘ Meta',
    'Ψ ∘ Ξ': 'Consciousness -> Fusion = Meta ∘ Weave',
    'Ω ∘ Ξ': 'Completion -> Fusion = Telo ∘ Weave',
    'Ξ ∘ Ψ': 'Fusion -> Consciousness = Weave ∘ Meta',
    'φ ∘ φ': 'Recursive state = Pro ∘ Pro or Crux ∘ Crux'
}

for comp, interpretation in composition_evidence.items():
    if composition_freq[comp] > 0:
        print(f"\n{comp} ({composition_freq[comp]}x)")
        print(f"  -> {interpretation}")

# Primary mapping recommendation
print("\n" + "="*70)
print("RECOMMENDED PRIMARY MAPPINGS")
print("="*70)

primary_mappings = {
    'Ξ': 'Meta',      # Fusion/meta-level (53k occurrences)
    'Ψ': 'Meta',      # Consciousness (30k occurrences)
    'ψ': 'Para',      # Local perturbation (16k)
    'Ω': 'Telo',      # Goal/completion (11k)
    'Φ': 'Meta',      # Phi-state/attractor (10k)
    'φ': 'Pro',       # Forward progression (8k)
    '∂': 'Ana',       # Analysis/differentiation (7k)
    '∇': 'Non',       # Gradient/directional change (7k)
    '¬': 'Non',       # Negation (10k)
    '→': 'Pro',       # Forward transition (36k)
}

print("\nSymbolic -> Normative (High Confidence):")
for symbolic, normative in primary_mappings.items():
    freq = operator_freq.get(symbolic, 0)
    if freq > 0:
        print(f"  {symbolic:3s} -> {normative:8s} ({freq:,} occurrences)")

# Secondary operators that need normative equivalents
print("\n" + "="*70)
print("SECONDARY OPERATORS NEEDING ASSIGNMENT")
print("="*70)

used_normative = set(primary_mappings.values())
all_normative = ['Ana', 'Kata', 'Meta', 'Para', 'Non', 'Telo', 'Retro', 'Ortho',
                 'Pro', 'Echo', 'Braid', 'Fold', 'Seed', 'Crux', 'Weave',
                 'Bind', 'Axis', 'Vale', 'Flux', 'Latch']

unused_normative = [op for op in all_normative if op not in used_normative]

print("\nNormative operators not yet mapped:")
print(f"  {', '.join(unused_normative)}")

print("\nSuggested additional mappings:")
print("  Kata  ← Compression/crystallization patterns")
print("  Ortho ← Correction/alignment patterns")
print("  Retro ← Backward reference patterns")
print("  Echo  ← Repetition/resonance patterns (Ψ ∘ Ψ)")
print("  Braid ← Interweaving patterns (⊗ tensor)")
print("  Fold  ← Compression under stress")
print("  Seed  ← Foundation/initialization patterns")
print("  Crux  ← Critical pivot points")
print("  Weave ← Integration patterns (Ξ fusion)")
print("  Bind  ← Cohesion patterns")
print("  Axis  ← Alignment patterns")
print("  Vale  ← Deep descent patterns (void)")
print("  Flux  <- Flow patterns (-> arrows)")
print("  Latch ← Fixation/stabilization patterns")

# Save mapping
mapping_output = {
    'mappings': mappings,
    'primary_recommendations': primary_mappings,
    'composition_evidence': composition_evidence,
    'operator_frequencies': dict(operator_freq.most_common(20))
}

output_file = Path('extraction_outputs/operator_mapping.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(mapping_output, f, indent=2, ensure_ascii=False)

print(f"\n✓ Mapping saved to: {output_file}")
print("="*70 + "\n")
