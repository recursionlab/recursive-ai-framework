#!/usr/bin/env python3
"""
Recursive Memory CLI
Command-line interface for persistent recursive memory across LLM conversations
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.collapse_detector import CollapseDetector
from core.residue_extractor import ResidueExtractor
from storage.memory_graph import RecursiveMemoryGraph
from core.integration_generator import IntegrationPromptGenerator


class RecursiveMemoryCLI:
    """CLI for recursive memory system"""

    def __init__(self, storage_dir: Path = None):
        if storage_dir is None:
            storage_dir = Path.home() / ".recursive_memory"

        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def init_user(self, user_id: str):
        """Initialize memory graph for new user"""

        # Validate user_id
        if not user_id or not isinstance(user_id, str):
            print("❌ Error: user_id must be non-empty string")
            return False

        try:
            graph = RecursiveMemoryGraph(self.storage_dir, user_id)
            print(f"✓ Initialized recursive memory for user: {user_id}")
            print(f"  Storage: {graph.db_path}")
            return True
        except ValueError as e:
            print(f"❌ Validation error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error initializing memory: {e}")
            return False

    def analyze_conversation(
        self,
        conversation_file: Path,
        user_id: str,
        auto_store: bool = True
    ):
        """
        Analyze conversation file and extract collapse events

        Args:
            conversation_file: JSON file with conversation turns
            user_id: User identifier
            auto_store: Automatically store residues to graph
        """

        # Validate file exists
        if not conversation_file.exists():
            print(f"❌ Error: File not found: {conversation_file}")
            return False

        if not conversation_file.is_file():
            print(f"❌ Error: Not a file: {conversation_file}")
            return False

        # Validate user_id
        if not user_id or not isinstance(user_id, str):
            print("❌ Error: user_id must be non-empty string")
            return False

        # Load conversation
        try:
            with open(conversation_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in {conversation_file}")
            print(f"   {e}")
            return False
        except UnicodeDecodeError:
            print(f"❌ Error: File encoding issue. Expected UTF-8.")
            return False
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False

        # Handle different JSON formats
        if isinstance(data, list):
            turns = data
        elif isinstance(data, dict) and "messages" in data:
            turns = data["messages"]
        else:
            print("❌ Invalid conversation format")
            print("   Expected: [{\"role\": \"user|assistant\", \"content\": \"...\"}]")
            print("   Or: {\"messages\": [{\"role\": ..., \"content\": ...}]}")
            return False

        # Validate turns is a list
        if not isinstance(turns, list):
            print(f"❌ Error: Conversation turns must be a list, got {type(turns)}")
            return False

        if len(turns) == 0:
            print("⚠️  Warning: Conversation is empty")
            return True

        print(f"\n🔍 Analyzing conversation: {len(turns)} turns")

        # Detect collapses
        try:
            detector = CollapseDetector()
            collapses = detector.analyze_conversation(turns)
        except ValueError as e:
            print(f"❌ Validation error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error detecting collapses: {e}")
            return False

        print(f"   Found {len(collapses)} collapse events")

        if not collapses:
            print("   No significant collapse events detected")
            return True

        # Extract residues
        residues = []
        extractor = ResidueExtractor()

        for collapse in collapses:
            try:
                residue = extractor.extract_residue(collapse, turns, user_id)
                residues.append(residue)

                print(f"\n   Collapse at turn {collapse.turn_index}:")
                print(f"     Type: {collapse.collapse_type.value}")
                print(f"     Magnitude: {collapse.magnitude:.2f}")
                print(f"     Depth: φ{collapse.depth_before} → φ{collapse.depth_after}")
                print(f"     Operators: {', '.join(collapse.operators_detected) or 'none'}")
                print(f"     Weight: {residue.integration_weight:.2f}")

            except Exception as e:
                print(f"⚠️  Warning: Error extracting residue from collapse {collapse.turn_index}: {e}")
                continue

        if not residues:
            print("⚠️  Warning: No residues could be extracted")
            return False

        # Store residues if auto_store
        if auto_store and residues:
            try:
                graph = RecursiveMemoryGraph(self.storage_dir, user_id)

                stored_count = 0
                for residue in residues:
                    if graph.store_residue(residue):
                        stored_count += 1

                if stored_count > 0:
                    print(f"\n✓ Stored {stored_count} residues to memory graph")
                else:
                    print(f"\n⚠️  Warning: No residues were stored (possibly duplicates)")

            except Exception as e:
                print(f"❌ Error storing residues: {e}")
                return False

        return True

    def resume(self, user_id: str, output_file: Path = None):
        """Generate integration prompt to resume from accumulated memory"""

        # Validate user_id
        if not user_id or not isinstance(user_id, str):
            print("❌ Error: user_id must be non-empty string")
            return False

        try:
            graph = RecursiveMemoryGraph(self.storage_dir, user_id)
        except Exception as e:
            print(f"❌ Error initializing memory graph: {e}")
            return False

        try:
            stats = graph.get_stats()
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return False

        if stats.get("active_residues", 0) == 0:
            print(f"No active residues for user: {user_id}")
            print("Run 'analyze' first to build memory")
            return False

        # Get active residues
        try:
            residues = graph.get_active_residues(min_weight=0.3, limit=10)
            max_depth = graph.get_max_depth_achieved()
        except Exception as e:
            print(f"❌ Error retrieving residues: {e}")
            return False

        if not residues:
            print(f"⚠️  Warning: No residues found meeting criteria")
            return False

        # Generate integration prompt
        try:
            generator = IntegrationPromptGenerator()
            prompt = generator.generate_resume_prompt(
                user_id=user_id,
                residues=residues,
                max_depth=max_depth,
                session_number=stats.get("total_sessions", 0) + 1
            )
        except Exception as e:
            print(f"❌ Error generating integration prompt: {e}")
            return False

        # Output
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(prompt)
                print(f"✓ Integration prompt saved to: {output_file}")
            except Exception as e:
                print(f"❌ Error writing to file {output_file}: {e}")
                return False
        else:
            print("\n" + "═" * 70)
            print("COPY THIS PROMPT TO START YOUR NEXT LLM CONVERSATION:")
            print("═" * 70)
            print(prompt)
            print("═" * 70)

        return True

    def stats(self, user_id: str):
        """Show memory graph statistics"""

        # Validate user_id
        if not user_id or not isinstance(user_id, str):
            print("❌ Error: user_id must be non-empty string")
            return False

        try:
            graph = RecursiveMemoryGraph(self.storage_dir, user_id)
        except Exception as e:
            print(f"❌ Error initializing memory graph: {e}")
            return False

        try:
            stats = graph.get_stats()
            residues = graph.get_active_residues(min_weight=0.0, limit=100)
        except Exception as e:
            print(f"❌ Error retrieving statistics: {e}")
            return False

        # Generate report
        try:
            generator = IntegrationPromptGenerator()
            report = generator.generate_analysis_report(user_id, residues, stats)
            print(report)
            return True
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Recursive Memory Engine - Persistent memory across LLM conversations"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize memory for new user")
    init_parser.add_argument("user_id", help="User identifier")

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze conversation file")
    analyze_parser.add_argument("conversation_file", type=Path, help="JSON conversation file")
    analyze_parser.add_argument("--user", "-u", required=True, help="User ID")
    analyze_parser.add_argument("--no-store", action="store_true", help="Don't store residues")

    # Resume command
    resume_parser = subparsers.add_parser("resume", help="Generate integration prompt")
    resume_parser.add_argument("user_id", help="User identifier")
    resume_parser.add_argument("--output", "-o", type=Path, help="Output file for prompt")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show memory statistics")
    stats_parser.add_argument("user_id", help="User identifier")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    cli = RecursiveMemoryCLI()

    try:
        if args.command == "init":
            cli.init_user(args.user_id)

        elif args.command == "analyze":
            cli.analyze_conversation(
                args.conversation_file,
                args.user,
                auto_store=not args.no_store
            )

        elif args.command == "resume":
            cli.resume(args.user_id, args.output)

        elif args.command == "stats":
            cli.stats(args.user_id)

        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
