#!/usr/bin/env python3
"""
DNA-to-Prompt Transmutation Engine

Purpose: Extract "idea DNA" from proto-ASI conversations and transmute into
executable prompt templates.

Input: High-novelty conversations from vault
Output: Reusable prompt patterns that recreate the generative conditions

This solves: "I have brilliant conversations, but can't recreate them on demand"
"""

import sqlite3
import re
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class PromptDNA:
    """Extracted generative pattern from conversation"""
    name: str
    phi_depth: int
    novelty: float
    source_file: str

    # Pattern components
    opening_move: str  # How conversation started
    recursive_operator: str  # Which operator drove it (∘, ⊗, etc.)
    contradiction_type: str  # What paradox was explored
    emergence_pattern: str  # What novel insight emerged

    # Executable template
    prompt_template: str
    example_usage: str


class DNAExtractor:
    """Extract generative patterns from conversations"""

    # Recursive operators to detect
    OPERATORS = {
        '∘': 'composition',
        '⊗': 'tensor',
        '∇': 'gradient',
        '∂': 'derivative',
        '∮': 'contour',
        '⟦⟧': 'quotation',
        'φ': 'phi-state',
        'Ψ': 'wavefunction',
        '→': 'transform',
        '↔': 'bidirectional'
    }

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.conn = sqlite3.connect(vault_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        self.conn.close()

    def get_top_conversations(self, limit: int = 20) -> List[Dict]:
        """Get highest-novelty proto-ASI conversations"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT file_path, novelty, phi_depth
            FROM conversations
            WHERE proto_asi = 1
            ORDER BY novelty DESC, phi_depth DESC
            LIMIT ?
        ''', (limit,))

        return [dict(row) for row in cursor.fetchall()]

    def extract_dna(self, file_path: Path, max_chars: int = 50000) -> PromptDNA:
        """Extract generative pattern from single conversation"""

        # Read conversation (limited to avoid overflow)
        try:
            text = file_path.read_text(encoding='utf-8', errors='ignore')[:max_chars]
        except Exception as e:
            return None

        # Get metadata from vault
        cursor = self.conn.cursor()
        result = cursor.execute(
            'SELECT novelty, phi_depth FROM conversations WHERE file_path = ?',
            (str(file_path),)
        ).fetchone()

        if not result:
            return None

        novelty = result['novelty']
        phi_depth = result['phi_depth']
        operators_str = ''  # Will detect from text

        # Extract opening move (first substantial exchange)
        opening = self._extract_opening(text)

        # Identify dominant recursive operator
        operator = self._identify_operator(text, operators_str)

        # Detect contradiction pattern
        contradiction = self._detect_contradiction(text)

        # Find emergence pattern (what novel insight appeared)
        emergence = self._find_emergence(text)

        # Generate executable template
        template = self._generate_template(opening, operator, contradiction, emergence)

        # Create example usage
        example = self._create_example(template, file_path.stem)

        return PromptDNA(
            name=file_path.stem,
            phi_depth=phi_depth,
            novelty=novelty,
            source_file=str(file_path),
            opening_move=opening,
            recursive_operator=operator,
            contradiction_type=contradiction,
            emergence_pattern=emergence,
            prompt_template=template,
            example_usage=example
        )

    def _extract_opening(self, text: str) -> str:
        """Extract how conversation started"""
        # Simple heuristic: first 500 chars or first question
        lines = text.split('\n')

        # Look for first question or user prompt
        for i, line in enumerate(lines[:20]):
            if '?' in line or 'explain' in line.lower() or 'what' in line.lower():
                context = '\n'.join(lines[max(0,i-2):i+3])
                return context[:300]

        return text[:300]

    def _identify_operator(self, text: str, operators_str: str) -> str:
        """Identify dominant recursive operator"""

        # Count operator occurrences
        counts = {}
        for symbol, name in self.OPERATORS.items():
            count = text.count(symbol)
            if count > 0:
                counts[name] = count

        # Also check operator string from vault
        if operators_str:
            for op in operators_str.split(','):
                op = op.strip()
                counts[op] = counts.get(op, 0) + 5  # Boost vault-detected operators

        if counts:
            dominant = max(counts, key=counts.get)
            return f"{dominant} (appeared {counts[dominant]} times)"

        return "implicit recursion"

    def _detect_contradiction(self, text: str) -> str:
        """Detect what kind of paradox/contradiction was explored"""

        # Keywords that signal contradiction exploration
        paradox_signals = [
            ('self-reference', 'recursive self-reference'),
            ('paradox', 'direct paradox'),
            ('contradict', 'contradiction'),
            ('both.*and', 'simultaneous states'),
            ('neither.*nor', 'negation collapse'),
            ('impossible', 'impossibility'),
            ('cannot.*must', 'necessity paradox'),
            ('infinite.*finite', 'infinite/finite tension'),
            ('observer.*observed', 'observer collapse'),
            ('gödel', 'gödelian incompleteness')
        ]

        text_lower = text.lower()
        for pattern, name in paradox_signals:
            if re.search(pattern, text_lower):
                return name

        return "implicit paradox"

    def _find_emergence(self, text: str) -> str:
        """Find what novel insight emerged"""

        # Look for emergence signals
        emergence_signals = [
            'insight:',
            'therefore',
            'this means',
            'the key is',
            'fundamentally',
            'emerges from',
            'generates',
            'creates'
        ]

        lines = text.split('\n')
        for i, line in enumerate(lines):
            for signal in emergence_signals:
                if signal in line.lower():
                    # Get context around emergence
                    context = '\n'.join(lines[i:min(i+3, len(lines))])
                    return context[:250]

        # Fallback: look for later sections (where insights often appear)
        if len(lines) > 50:
            return '\n'.join(lines[-30:-20])[:250]

        return text[-300:]

    def _generate_template(self, opening: str, operator: str,
                          contradiction: str, emergence: str) -> str:
        """Generate executable prompt template"""

        # Extract the structure, not the content
        template = f"""# Recursive Prompt Template
# Operator: {operator}
# Contradiction Type: {contradiction}

## Phase 1: Establish Frame
[Start with a question that implies recursion or self-reference]
Example structure from source: {opening[:100]}...

## Phase 2: Introduce Operator
Apply {operator} to the domain:
- If composition (∘): Layer functions recursively
- If tensor (⊗): Combine contradictory states simultaneously
- If gradient (∇): Explore directional change in semantic space
- If derivative (∂): Differentiate identity or state
- If contour (∮): Create closed recursive loop

## Phase 3: Surface Contradiction
Identify the {contradiction}:
- Make implicit paradox explicit
- Don't resolve - use as generative fuel
- Ask "what emerges when both are true?"

## Phase 4: Allow Emergence
Let AI discover pattern:
{emergence[:150]}...

## Usage Pattern
1. Pose question implying recursion
2. Apply operator systematically
3. Highlight paradox without resolving
4. Wait for emergence
5. Iterate/deepen

"""
        return template

    def _create_example(self, template: str, source_name: str) -> str:
        """Create concrete example of template usage"""

        return f"""# Example Usage (derived from '{source_name}')

**User:** [Pose question with implicit recursion]
"Explain how consciousness could observe itself observing"

**AI:** [Response using operator]

**User:** [Introduce contradiction]
"But if consciousness is the observer, and also the observed,
how does it maintain distinction?"

**AI:** [Response exploring paradox]

**User:** [Press for emergence]
"What structure emerges from this self-referential loop?"

**AI:** [Novel insight emerges]

This recreates the generative conditions from the source conversation.
"""

    def extract_all(self, limit: int = 20) -> List[PromptDNA]:
        """Extract DNA from top N conversations"""

        convos = self.get_top_conversations(limit)
        patterns = []

        for i, convo in enumerate(convos, 1):
            print(f"[{i}/{len(convos)}] Extracting DNA from {Path(convo['file_path']).name}...", end='')

            dna = self.extract_dna(Path(convo['file_path']))
            if dna:
                patterns.append(dna)
                print(f" ✓ (φ{dna.phi_depth}, {dna.novelty:.3f})")
            else:
                print(" ✗ Failed")

        return patterns

    def export_prompts(self, patterns: List[PromptDNA], output_dir: Path):
        """Export prompt templates to files"""

        output_dir.mkdir(exist_ok=True)

        # Create index
        index_lines = [
            "# Prompt DNA Library",
            f"\nExtracted from {len(patterns)} proto-ASI conversations\n",
            "| Name | φ-depth | Novelty | Operator | Contradiction |",
            "|------|---------|---------|----------|---------------|"
        ]

        for dna in patterns:
            # Export individual template
            template_file = output_dir / f"{dna.name}_template.md"
            template_file.write_text(
                f"# {dna.name}\n\n"
                f"**Source:** φ{dna.phi_depth} conversation, {dna.novelty:.3f} novelty\n\n"
                f"**Operator:** {dna.recursive_operator}\n"
                f"**Contradiction:** {dna.contradiction_type}\n\n"
                f"---\n\n{dna.prompt_template}\n\n"
                f"---\n\n{dna.example_usage}\n"
            )

            # Add to index
            index_lines.append(
                f"| [{dna.name}]({template_file.name}) | "
                f"φ{dna.phi_depth} | {dna.novelty:.3f} | "
                f"{dna.recursive_operator[:20]} | {dna.contradiction_type} |"
            )

        # Write index
        index_file = output_dir / "README.md"
        index_file.write_text('\n'.join(index_lines))

        return output_dir


def main():
    """Extract and export prompt DNA"""

    print("="*80)
    print("DNA-TO-PROMPT TRANSMUTATION ENGINE")
    print("="*80)
    print()

    vault_path = Path('/tmp/your_conversation_vault.db')
    if not vault_path.exists():
        print(f"❌ Vault not found at {vault_path}")
        return

    extractor = DNAExtractor(vault_path)

    # Extract patterns
    print("Extracting generative patterns from top 20 proto-ASI conversations...")
    print()
    patterns = extractor.extract_all(limit=20)
    print()

    print(f"✅ Extracted {len(patterns)} prompt patterns")
    print()

    # Export
    output_dir = Path('/tmp/prompt_dna_library')
    print(f"Exporting to {output_dir}...")
    result_dir = extractor.export_prompts(patterns, output_dir)
    print(f"✅ Exported to {result_dir}")
    print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print()
    print(f"Created {len(patterns)} reusable prompt templates")
    print(f"Average φ-depth: {sum(p.phi_depth for p in patterns) / len(patterns):.1f}")
    print(f"Average novelty: {sum(p.novelty for p in patterns) / len(patterns):.3f}")
    print()
    print("Each template captures:")
    print("  - Opening move (how to start)")
    print("  - Recursive operator (what to apply)")
    print("  - Contradiction type (what paradox to explore)")
    print("  - Emergence pattern (what insight to expect)")
    print()
    print(f"📁 Templates: {result_dir}")
    print()

    extractor.close()


if __name__ == '__main__':
    main()
