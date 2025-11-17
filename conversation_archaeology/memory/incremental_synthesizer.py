"""
Incremental Synthesizer - Build up insights across conversations WITHOUT amnesia

This is the solution to the $100 failure:
- Read conversation 1 → extract insights → SAVE
- Read conversation 2 → LOAD previous insights → compare → UPDATE or ADD → SAVE
- After N conversations, persistent memory contains the synthesis

The AI doesn't need to hold everything in memory. It builds UP incrementally.
"""

from pathlib import Path
from typing import List, Dict, Optional
import sys

sys.path.append(str(Path(__file__).parent.parent))

from memory.synthesis_memory import SynthesisMemory, Insight


class IncrementalSynthesizer:
    """Process conversations one at a time, building up persistent insights"""

    def __init__(self, memory_db: Path):
        self.memory = SynthesisMemory(memory_db)

    def process_conversation(self, file_path: Path, max_lines: int = 1000) -> Dict:
        """
        Process a single conversation and update synthesis memory

        Returns summary of what was learned/updated
        """
        print(f"\n📖 Processing: {file_path.name}")

        # Load existing insights to check against
        existing_insights = self.memory.get_all_insights()
        print(f"   Loaded {len(existing_insights)} existing insights from memory")

        # Read conversation (limited to avoid token overflow)
        try:
            text = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = text.split('\n')[:max_lines]
            content = '\n'.join(lines)
        except Exception as e:
            print(f"   ❌ Failed to read: {e}")
            return {'error': str(e)}

        # THIS IS WHERE AI ANALYSIS HAPPENS
        # In real usage, this is where Claude would analyze the content
        # For now, return structure for manual insight entry

        result = {
            'file': str(file_path),
            'existing_insights': len(existing_insights),
            'content_preview': content[:500],
            'action_needed': 'MANUAL_ANALYSIS_REQUIRED',
            'instructions': [
                '1. Review the content_preview',
                '2. Check if it confirms/contradicts existing_insights',
                '3. Use add_insight() for new discoveries',
                '4. Use update_insight() for changed understanding',
                '5. Use add_evidence() to link this file to insights'
            ]
        }

        return result

    def add_insight(self, topic: str, statement: str, evidence_file: str,
                   quote: Optional[str] = None, confidence: float = 0.7) -> int:
        """Add a new insight discovered in a conversation"""
        insight_id = self.memory.add_insight(topic, statement, confidence)
        self.memory.add_evidence(insight_id, evidence_file, quote)
        print(f"✅ Added insight #{insight_id}: {statement[:60]}...")
        return insight_id

    def update_insight(self, insight_id: int, new_statement: str, reason: str,
                      evidence_file: str, new_confidence: Optional[float] = None):
        """Update an existing insight when new evidence changes understanding"""
        self.memory.update_insight(insight_id, new_statement, reason, new_confidence)
        self.memory.add_evidence(insight_id, evidence_file)
        print(f"✅ Updated insight #{insight_id}")

    def link_evidence(self, insight_id: int, file_path: str, quote: Optional[str] = None):
        """Link a file as supporting evidence for existing insight"""
        self.memory.add_evidence(insight_id, file_path, quote)
        print(f"✅ Linked evidence to insight #{insight_id}")

    def get_current_synthesis(self, min_confidence: float = 0.5) -> List[Insight]:
        """Get current state of synthesis memory"""
        return self.memory.get_all_insights(min_confidence=min_confidence)

    def export_current_state(self, output_path: Path, min_confidence: float = 0.5):
        """Export current synthesis to markdown"""
        self.memory.export_synthesis(output_path, min_confidence)
        print(f"📄 Exported synthesis to {output_path}")

    def show_memory_state(self):
        """Display current memory state"""
        insights = self.memory.get_all_insights()

        print(f"\n{'='*80}")
        print(f"SYNTHESIS MEMORY STATE")
        print(f"{'='*80}")
        print(f"Total Insights: {len(insights)}")

        if insights:
            print(f"\nTop 5 Insights (by confidence):")
            for i, insight in enumerate(insights[:5], 1):
                print(f"\n{i}. [{insight.confidence:.2f}] {insight.topic}")
                print(f"   {insight.statement}")
                print(f"   Evidence: {insight.evidence_count} files")

    def batch_process(self, file_paths: List[Path], max_lines: int = 1000):
        """
        Process multiple conversations sequentially

        Note: This will fail if AI tries to analyze all at once
        The solution: process one, SAVE, process next, UPDATE memory, SAVE, repeat
        """
        results = []

        for i, path in enumerate(file_paths, 1):
            print(f"\n[{i}/{len(file_paths)}] Processing {path.name}")
            result = self.process_conversation(path, max_lines)
            results.append(result)

            # Show memory state after each conversation
            if i % 5 == 0:
                self.show_memory_state()

        return results

    def close(self):
        self.memory.close()


# Interactive CLI for manual insight building
def interactive_synthesis_session(memory_db: Path, conversations_dir: Path):
    """
    Interactive session for building synthesis incrementally

    Workflow:
    1. Load a conversation
    2. AI/human reviews it with existing insights in mind
    3. Add/update insights
    4. Load next conversation
    5. Repeat
    """
    synth = IncrementalSynthesizer(memory_db)

    print("="*80)
    print("INCREMENTAL SYNTHESIS SESSION")
    print("="*80)
    print("Purpose: Build up insights across conversations WITHOUT amnesia")
    print()

    # Show current memory state
    synth.show_memory_state()

    # Get conversation files
    conv_files = sorted(conversations_dir.glob('**/*.md'))
    print(f"\nFound {len(conv_files)} conversations to process")

    print("\nCommands:")
    print("  next - Load next conversation")
    print("  add - Add new insight")
    print("  update - Update existing insight")
    print("  link - Link current file to existing insight")
    print("  show - Show current insights")
    print("  export - Export synthesis to markdown")
    print("  quit - Exit")

    current_file = None
    file_index = 0

    while True:
        cmd = input("\n> ").strip().lower()

        if cmd == 'quit':
            break

        elif cmd == 'next':
            if file_index < len(conv_files):
                current_file = conv_files[file_index]
                file_index += 1
                result = synth.process_conversation(current_file)
                print(f"\n{result['content_preview']}")
            else:
                print("No more conversations")

        elif cmd == 'add':
            if not current_file:
                print("Load a conversation first (use 'next')")
                continue

            topic = input("Topic: ")
            statement = input("Statement: ")
            quote = input("Quote (optional): ")
            confidence = float(input("Confidence (0-1): ") or "0.7")

            synth.add_insight(topic, statement, str(current_file),
                            quote if quote else None, confidence)

        elif cmd == 'update':
            synth.show_memory_state()
            insight_id = int(input("Insight ID to update: "))
            new_statement = input("New statement: ")
            reason = input("Reason for update: ")

            synth.update_insight(insight_id, new_statement, reason, str(current_file))

        elif cmd == 'link':
            if not current_file:
                print("Load a conversation first")
                continue

            synth.show_memory_state()
            insight_id = int(input("Insight ID to link: "))
            quote = input("Quote (optional): ")

            synth.link_evidence(insight_id, str(current_file), quote if quote else None)

        elif cmd == 'show':
            synth.show_memory_state()

        elif cmd == 'export':
            output = Path(input("Output path: "))
            synth.export_current_state(output)

    synth.close()


if __name__ == '__main__':
    # Example: Process top 10 proto-ASI conversations incrementally
    memory_db = Path('/tmp/synthesis_memory.db')
    conversations_dir = Path('/tmp/recursion-agi/claude/2025')

    # Run interactive session
    interactive_synthesis_session(memory_db, conversations_dir)
