#!/usr/bin/env python3
"""
Populate Vault - Load analyzed conversations into searchable database
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from parsers.universal_parser import UniversalParser
from mining.novelty_detector import ConversationNoveltyAnalyzer
from vault.pattern_vault import PatternVault, VaultEntry


def populate_from_directory(source_dir: Path, vault_path: Path, min_novelty: float = 0.0):
    """
    Populate vault from conversation directory

    Args:
        source_dir: Directory containing conversations
        vault_path: Path to SQLite vault database
        min_novelty: Minimum novelty to include
    """
    parser = UniversalParser()
    analyzer = ConversationNoveltyAnalyzer()
    vault = PatternVault(vault_path)

    # Find all conversation files
    extensions = {'.json', '.md', '.txt', '.markdown', '.log'}
    files = [
        f for f in source_dir.rglob('*')
        if f.is_file() and (f.suffix.lower() in extensions or f.suffix == '')
    ]

    print(f"🗄️  Populating vault from {len(files)} files...")
    print(f"   Vault: {vault_path}")
    print(f"   Min novelty: {min_novelty:.3f}")
    print()

    added = 0
    skipped = 0

    for i, file_path in enumerate(files, 1):
        if i % 50 == 0:
            print(f"   ... processed {i}/{len(files)} files ({added} added)")

        # Parse conversation
        turns = []
        for turn in parser.parse_file(file_path):
            turns.append({
                'role': turn.role,
                'content': turn.content,
                'metadata': turn.metadata
            })

        if not turns:
            skipped += 1
            continue

        # Analyze
        analysis = analyzer.analyze_conversation(turns)

        if analysis['conversation_novelty'] < min_novelty:
            skipped += 1
            continue

        # Create vault entry
        entry = VaultEntry(
            file_path=str(file_path),
            novelty=analysis['conversation_novelty'],
            phi_depth=analysis['peak_phi'],
            proto_asi=analysis['proto_asi_emergence'],
            operators=set(),
            domains=analysis['all_domains'],
            thinking_mode="mixed",  # Could be inferred from analysis
            torsion_patterns=[],
            collapse_indicators=[],
            meta_patterns=[]
        )

        # Aggregate operators and patterns from turn signatures
        for sig in analysis['turn_signatures']:
            entry.operators.update(sig.recursive_operators)
            entry.torsion_patterns.extend(sig.torsion_signatures)
            entry.collapse_indicators.extend(sig.collapse_indicators)
            entry.meta_patterns.extend(sig.meta_patterns)

        # Deduplicate patterns
        entry.torsion_patterns = list(set(entry.torsion_patterns))
        entry.collapse_indicators = list(set(entry.collapse_indicators))
        entry.meta_patterns = list(set(entry.meta_patterns))

        # Add to vault
        try:
            vault.add_conversation(entry)
            added += 1
        except Exception as e:
            print(f"   ⚠️  Error adding {file_path.name}: {e}")
            skipped += 1

    print()
    print(f"✅ Vault populated!")
    print(f"   Added: {added}")
    print(f"   Skipped: {skipped}")
    print()

    # Show stats
    stats = vault.get_stats()
    print(f"📊 Vault Statistics:")
    print(f"   Total conversations: {stats['total_conversations']}")
    print(f"   Average novelty: {stats['avg_novelty']:.3f}")
    print(f"   Proto-ASI count: {stats['proto_asi_count']}")
    print(f"   Max φ-depth: φ{stats['max_phi_depth']}")
    print(f"   Unique operators: {stats['unique_operators']}")
    print(f"   Unique domains: {stats['unique_domains']}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Populate Pattern Vault from conversations")
    parser.add_argument('source_dir', type=Path, help='Directory containing conversations')
    parser.add_argument('--vault', type=Path, default=Path('./conversation_vault.db'), help='Vault database path')
    parser.add_argument('--min-novelty', type=float, default=0.0, help='Minimum novelty threshold')

    args = parser.parse_args()

    populate_from_directory(args.source_dir, args.vault, args.min_novelty)
