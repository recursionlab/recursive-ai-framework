#!/usr/bin/env python3
"""
Core Mechanism Extractor

Purpose: Go beyond templates - extract the ACTUAL MECHANISM that makes
high-novelty conversations generative.

Not "what did they say" but "what cognitive operation generated novelty"

This answers: What recursive operator is ACTUALLY running underneath?
"""

import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple
import re
from collections import Counter


class CoreMechanismExtractor:
    """Extract the generative mechanism from conversations"""

    # Core recursive operators (the actual machines)
    OPERATORS = {
        'self_application': r'(?:apply|applying|applies) (?:to|on) itself',
        'negation_fold': r'not.{1,30}not|¬.{1,30}¬|contradiction',
        'meta_layer': r'meta-|about.{1,20}about|of.{1,20}of',
        'recursive_loop': r'recur(?:sive|sion)|loop|cycle|iterate',
        'collapse_rebirth': r'collapse|emerge|generate|birth',
        'inversion': r'invert|reverse|flip|opposite',
        'composition': r'compose|combine|merge|fuse',
        'fixpoint': r'fixed.{1,10}point|stable|attractor|converge',
    }

    # Generative patterns (what actually creates novelty)
    GENERATIVE_PATTERNS = {
        'paradox_fuel': r'paradox|contradiction.{1,30}(?:fuel|generate|create)',
        'observer_observed': r'observer.{1,30}observed|watch.{1,30}watching',
        'map_territory': r'map.{1,30}territory|model.{1,30}reality',
        'self_reference': r'self.{1,10}referen|recursive.{1,10}self',
        'infinite_regress': r'infinite.{1,20}regress|turtles.{1,20}down',
        'category_violation': r'category.{1,20}(?:error|violation|confusion)',
        'frame_breaking': r'break.{1,10}frame|transcend.{1,10}boundary',
        'dimension_shift': r'dimension|layer|level|plane',
    }

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.conn = sqlite3.connect(vault_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        self.conn.close()

    def extract_mechanism(self, file_path: Path, max_chars: int = 100000) -> Dict:
        """Extract the core generative mechanism from a conversation"""

        try:
            text = file_path.read_text(encoding='utf-8', errors='ignore')[:max_chars]
        except Exception:
            return None

        # Detect operators
        operators = {}
        for op_name, pattern in self.OPERATORS.items():
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            if matches > 0:
                operators[op_name] = matches

        # Detect generative patterns
        patterns = {}
        for pattern_name, pattern_re in self.GENERATIVE_PATTERNS.items():
            matches = len(re.findall(pattern_re, text, re.IGNORECASE))
            if matches > 0:
                patterns[pattern_name] = matches

        # Extract example phrases showing mechanism in action
        examples = self._extract_mechanism_examples(text)

        # Identify the dominant mechanism
        dominant_operator = max(operators.items(), key=lambda x: x[1])[0] if operators else 'unknown'
        dominant_pattern = max(patterns.items(), key=lambda x: x[1])[0] if patterns else 'unknown'

        return {
            'file': str(file_path),
            'dominant_operator': dominant_operator,
            'dominant_pattern': dominant_pattern,
            'operators': operators,
            'patterns': patterns,
            'examples': examples,
            'mechanism_signature': f"{dominant_operator}+{dominant_pattern}"
        }

    def _extract_mechanism_examples(self, text: str) -> List[str]:
        """Extract actual examples of mechanism in action"""

        examples = []

        # Look for sentences with high operator density
        sentences = re.split(r'[.!?]\s+', text)

        for sentence in sentences[:500]:  # Check first 500 sentences
            if len(sentence) < 50 or len(sentence) > 300:
                continue

            # Count operator occurrences
            op_count = sum(
                len(re.findall(pattern, sentence, re.IGNORECASE))
                for pattern in self.OPERATORS.values()
            )

            pattern_count = sum(
                len(re.findall(pattern, sentence, re.IGNORECASE))
                for pattern in self.GENERATIVE_PATTERNS.values()
            )

            # High-density sentences likely demonstrate mechanism
            if op_count + pattern_count >= 3:
                examples.append(sentence.strip())

            if len(examples) >= 5:
                break

        return examples

    def analyze_top_conversations(self, limit: int = 20) -> List[Dict]:
        """Analyze top conversations to extract mechanisms"""

        cursor = self.conn.cursor()

        top_convos = cursor.execute('''
            SELECT file_path, phi_depth, novelty
            FROM conversations
            WHERE proto_asi = 1 AND novelty > 0.85
            ORDER BY novelty DESC, phi_depth DESC
            LIMIT ?
        ''', (limit,)).fetchall()

        mechanisms = []

        for i, convo in enumerate(top_convos, 1):
            print(f"[{i}/{len(top_convos)}] Extracting mechanism from {Path(convo['file_path']).name}...", end='')

            mechanism = self.extract_mechanism(Path(convo['file_path']))

            if mechanism:
                mechanism['phi_depth'] = convo['phi_depth']
                mechanism['novelty'] = convo['novelty']
                mechanisms.append(mechanism)
                print(f" ✓ {mechanism['mechanism_signature']}")
            else:
                print(" ✗")

        return mechanisms

    def synthesize_meta_mechanism(self, mechanisms: List[Dict]) -> Dict:
        """Synthesize the underlying meta-mechanism from all conversations"""

        # Aggregate operators
        all_operators = Counter()
        all_patterns = Counter()

        for mech in mechanisms:
            all_operators.update(mech['operators'])
            all_patterns.update(mech['patterns'])

        # Find mechanism signatures (combinations that appear together)
        signature_freq = Counter(m['mechanism_signature'] for m in mechanisms)

        # Identify the universal recursive engine
        top_operators = dict(all_operators.most_common(5))
        top_patterns = dict(all_patterns.most_common(5))
        top_signatures = dict(signature_freq.most_common(10))

        return {
            'universal_operators': top_operators,
            'universal_patterns': top_patterns,
            'common_signatures': top_signatures,
            'total_analyzed': len(mechanisms)
        }

    def generate_executable_core(self, meta_mechanism: Dict) -> str:
        """Generate executable description of the core mechanism"""

        operators = meta_mechanism['universal_operators']
        patterns = meta_mechanism['universal_patterns']

        # The actual mechanism
        core = f"""# The Core Recursive Mechanism

From {meta_mechanism['total_analyzed']} high-novelty conversations.

## Universal Operators (What Actually Runs)

"""

        for op, count in operators.items():
            core += f"- **{op.replace('_', ' ').title()}**: {count} occurrences\n"

        core += "\n## Generative Patterns (What Creates Novelty)\n\n"

        for pattern, count in patterns.items():
            core += f"- **{pattern.replace('_', ' ').title()}**: {count} occurrences\n"

        core += """

## The Unified Mechanism

High-novelty conversations share a common recursive engine:

1. **Start with self-application** - Apply concept to itself
2. **Introduce meta-layer** - Ask "what about the asking"
3. **Create recursive loop** - Feed output back as input
4. **Encounter paradox** - Reach contradiction or limit
5. **Use paradox as fuel** - Don't resolve, leverage for generation
6. **Collapse and rebirth** - System reorganizes at higher level

This is not sequential - it's a **recursive field** where each operation
feeds back into all others simultaneously.

## Executable Form

```
ΞRecursiveMechanism(x):
    while not_converged(x):
        x = apply(x, to=x)           # Self-application
        x = meta(x)                  # Meta-layer
        if paradox(x):
            x = fuel(x, with=paradox) # Paradox-as-fuel
            x = collapse(x)           # Collapse
            x = emerge(x)             # Rebirth
    return fixpoint(x)
```

The mechanism doesn't SOLVE problems - it EVOLVES them into higher forms.
"""

        return core

    def export_mechanisms(self, mechanisms: List[Dict], output_dir: Path):
        """Export mechanism analysis"""

        output_dir.mkdir(exist_ok=True, parents=True)

        # Export individual mechanisms
        mechanisms_file = output_dir / 'mechanisms.jsonl'
        with mechanisms_file.open('w') as f:
            import json
            for mech in mechanisms:
                # Remove examples for cleaner export
                mech_clean = {k: v for k, v in mech.items() if k != 'examples'}
                f.write(json.dumps(mech_clean) + '\n')

        # Generate meta-mechanism
        meta = self.synthesize_meta_mechanism(mechanisms)

        # Generate executable core
        core = self.generate_executable_core(meta)

        core_file = output_dir / 'CORE_MECHANISM.md'
        core_file.write_text(core)

        print(f"\n✅ Mechanisms exported to {output_dir}")
        print(f"📄 Core mechanism: {core_file}")
        print(f"📊 Raw data: {mechanisms_file}")

        return core_file


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Extract core mechanisms')
    parser.add_argument('--vault-db', type=Path, default=Path('/tmp/your_conversation_vault.db'))
    parser.add_argument('--output-dir', type=Path, default=Path('/tmp/core_mechanisms'))
    parser.add_argument('--limit', type=int, default=30, help='Number of conversations to analyze')

    args = parser.parse_args()

    print("="*80)
    print("CORE MECHANISM EXTRACTOR")
    print("="*80)
    print()

    if not args.vault_db.exists():
        print(f"❌ Vault not found at {args.vault_db}")
        return

    extractor = CoreMechanismExtractor(args.vault_db)

    try:
        # Extract mechanisms
        print(f"Analyzing top {args.limit} conversations...")
        print()
        mechanisms = extractor.analyze_top_conversations(limit=args.limit)

        print()
        print(f"✅ Extracted {len(mechanisms)} mechanisms")
        print()

        # Export
        core_file = extractor.export_mechanisms(mechanisms, args.output_dir)

        print()
        print("="*80)
        print("EXTRACTION COMPLETE")
        print("="*80)
        print()
        print(f"🧬 Core mechanism: {core_file}")

    finally:
        extractor.close()


if __name__ == '__main__':
    main()
