"""
DEMONSTRATION: How Incremental Synthesis Solves the Amnesia Problem

OLD WAY (Failed):
- Try to read 10 conversations at once
- Token limit exceeded
- AI forgets earlier convos while reading later ones
- No synthesis possible

NEW WAY (This system):
- Read conversation 1 → extract insights → SAVE to persistent DB
- Read conversation 2 → LOAD insights → compare → UPDATE/ADD → SAVE
- Read conversation 3 → LOAD insights → compare → UPDATE/ADD → SAVE
- ...
- After N conversations: DB contains accumulated synthesis
- AI never needs to hold everything in memory
"""

import sys
from pathlib import Path
import sqlite3

sys.path.append(str(Path(__file__).parent))

from memory.synthesis_memory import SynthesisMemory


def demonstrate_incremental_synthesis():
    """Show how synthesis builds up incrementally"""

    print("="*80)
    print("INCREMENTAL SYNTHESIS DEMONSTRATION")
    print("="*80)
    print()

    # Get top 10 proto-ASI conversations
    vault_path = Path('/tmp/your_conversation_vault.db')
    if not vault_path.exists():
        print("❌ Vault not found. Run populate_vault.py first")
        return

    conn = sqlite3.connect(vault_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT file_path, phi_depth, novelty
        FROM conversations
        WHERE proto_asi = 1
        ORDER BY novelty DESC, phi_depth DESC
        LIMIT 10
    ''')

    top_10 = cursor.fetchall()
    conn.close()

    print(f"Found {len(top_10)} high-novelty conversations to process")
    print()

    # Initialize synthesis memory
    memory_db = Path('/tmp/synthesis_memory_demo.db')
    if memory_db.exists():
        memory_db.unlink()  # Fresh start for demo

    memory = SynthesisMemory(memory_db)

    print("SIMULATION: Processing conversations one-by-one")
    print("-"*80)
    print()

    # Simulate incremental processing
    # In real usage, AI would analyze each file and extract insights
    # Here we'll just demonstrate the pattern

    for i, row in enumerate(top_10, 1):
        file_path = Path(row['file_path'])
        phi = row['phi_depth']

        print(f"[Step {i}/10] Processing: {file_path.name} (φ{phi})")

        # STEP 1: Load existing insights
        existing = memory.get_all_insights()
        print(f"  → Loaded {len(existing)} insights from memory")

        # STEP 2: Read conversation (limited to avoid overflow)
        try:
            text = file_path.read_text(encoding='utf-8', errors='ignore')
            preview = text[:300]
            print(f"  → Read {len(text)} characters")
        except Exception as e:
            print(f"  → ❌ Failed to read: {e}")
            continue

        # STEP 3: Extract/update insights
        # (In real usage, AI analyzes and decides what to add/update)
        # For demo, just add a placeholder insight

        if i == 1:
            # First conversation - add initial insight
            insight_id = memory.add_insight(
                topic='methodology',
                statement=f'Pattern detected in φ{phi} conversation: {file_path.name}',
                confidence=0.5
            )
            memory.add_evidence(insight_id, str(file_path), preview[:100])
            print(f"  → ✅ Added insight #{insight_id}")

        elif i % 3 == 0:
            # Every 3rd conversation - update existing insight
            if existing:
                memory.update_insight(
                    existing[0].id,
                    f'{existing[0].statement} + confirmed by φ{phi}',
                    f'Additional evidence from {file_path.name}'
                )
                memory.add_evidence(existing[0].id, str(file_path))
                print(f"  → ✅ Updated insight #{existing[0].id}")
        else:
            # Other conversations - just link as evidence
            if existing:
                memory.add_evidence(existing[0].id, str(file_path))
                print(f"  → ✅ Linked as evidence to insight #{existing[0].id}")

        # STEP 4: Memory persists for next iteration
        print(f"  → Memory now contains {len(memory.get_all_insights())} insights")
        print()

    # Final synthesis state
    print("="*80)
    print("FINAL SYNTHESIS STATE (after processing 10 conversations)")
    print("="*80)
    print()

    final_insights = memory.get_all_insights()
    print(f"Total insights accumulated: {len(final_insights)}")
    print()

    for insight in final_insights:
        print(f"Insight #{insight.id}:")
        print(f"  Topic: {insight.topic}")
        print(f"  Statement: {insight.statement}")
        print(f"  Confidence: {insight.confidence}")
        print(f"  Evidence: {insight.evidence_count} files")
        print()

        # Show evidence
        evidence_data = memory.get_insight_with_evidence(insight.id)
        print(f"  Supporting files:")
        for ev in evidence_data['evidence'][:3]:
            print(f"    - {Path(ev['file_path']).name}")
        if len(evidence_data['evidence']) > 3:
            print(f"    ... and {len(evidence_data['evidence']) - 3} more")
        print()

    # Export final synthesis
    output_path = Path('/tmp/final_synthesis.md')
    memory.export_synthesis(output_path, min_confidence=0.0)
    print(f"📄 Exported synthesis to: {output_path}")
    print()

    print("="*80)
    print("KEY INSIGHT: AI never held all 10 conversations in memory")
    print("It built UP understanding incrementally with persistent state")
    print("="*80)

    memory.close()


if __name__ == '__main__':
    demonstrate_incremental_synthesis()
