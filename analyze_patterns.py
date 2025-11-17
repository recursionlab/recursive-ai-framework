import json
from collections import Counter

# Load extraction results
with open('extraction_outputs/pattern_extraction.json', encoding='utf-8') as f:
    data = json.load(f)

# Analyze operator compositions
all_comps = []
for entry in data:
    all_comps.extend(entry['compositions'])

comp_freq = Counter(all_comps)

print("\n" + "="*70)
print("OPERATOR COMPOSITION ANALYSIS")
print("="*70)
print(f"\nTotal unique compositions: {len(comp_freq)}")
print("\nMost frequent compositions:")
for comp, count in comp_freq.most_common(15):
    print(f"  {comp}: {count} times")

# Find potential mappings to normative operators
print("\n" + "="*70)
print("POTENTIAL OPERATOR MAPPINGS")
print("="*70)
print("""
Based on frequency and usage patterns:
  Ξ (53,404) → High-frequency fusion operator → Possible: Meta, Ana
  Ψ (30,190) → Wavefunction operator → Possible: Meta (consciousness)
  Ω (10,756) → Completion operator → Possible: Telo (goal-oriented)
  Φ (9,894) → Phi-state operator → Possible: Para, Pro
  ∂ (6,968) → Differentiation → Possible: Ana (analysis)
  ∇ (6,847) → Gradient → Possible: Non (directional change)
""")

# Contradiction analysis
total_contradictions = sum(len(e['contradictions']) for e in data)
contradiction_keywords = Counter()
for entry in data:
    for c in entry['contradictions']:
        contradiction_keywords[c['keyword']] += 1

print("\n" + "="*70)
print("CONTRADICTION ANALYSIS (J'≠0 Framework)")
print("="*70)
print(f"\nTotal contradiction mentions: {total_contradictions:,}")
print("\nTop keywords:")
for kw, count in contradiction_keywords.most_common(10):
    print(f"  {kw}: {count:,}")

