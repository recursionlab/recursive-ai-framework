#!/usr/bin/env python3
"""
Full Conversation Archaeology Pipeline

Runs complete analysis on conversation corpus:
1. Mine conversations → statistics and clusters
2. Extract DNA → prompt templates
3. Extract mechanisms → universal recursive operators
4. Map connections → shared concepts and evolution chains
5. Analyze meta-patterns → corpus-wide insights
6. Integrate synthesis → persistent memory
7. Generate visualizations → charts and networks

Usage:
    python run_full_analysis.py /path/to/conversations --output /path/to/results

This is the "push button" archaeology system.
"""

import argparse
import subprocess
from pathlib import Path
import sys
from datetime import datetime


class ArchaeologyPipeline:
    """Orchestrate full archaeology analysis"""

    def __init__(self, conversation_dir: Path, output_dir: Path):
        self.conversation_dir = conversation_dir
        self.output_dir = output_dir
        self.tools_dir = Path(__file__).parent / 'tools'
        self.vault_db = output_dir / 'conversation_vault.db'
        self.synthesis_db = output_dir / 'synthesis_memory.db'

    def run_step(self, name: str, command: list, critical: bool = True) -> bool:
        """Run a pipeline step"""
        print()
        print("="*80)
        print(f"STEP: {name}")
        print("="*80)
        print(f"Command: {' '.join(str(c) for c in command)}")
        print()

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ FAILED: {name}")
            print(result.stderr)
            if critical:
                print(f"\n⚠️  Critical step failed, aborting pipeline")
                return False
            else:
                print(f"\n⚠️  Non-critical step failed, continuing...")
        else:
            print(result.stdout)
            print(f"✅ COMPLETED: {name}")

        return True

    def run(self) -> bool:
        """Execute full pipeline"""

        start_time = datetime.now()

        print("="*80)
        print("CONVERSATION ARCHAEOLOGY FULL PIPELINE")
        print("="*80)
        print()
        print(f"Conversation Directory: {self.conversation_dir}")
        print(f"Output Directory: {self.output_dir}")
        print(f"Vault Database: {self.vault_db}")
        print(f"Synthesis Database: {self.synthesis_db}")
        print()
        print(f"Started: {start_time.isoformat()}")
        print()

        self.output_dir.mkdir(exist_ok=True, parents=True)

        # Step 1: Build conversation vault (if doesn't exist)
        if not self.vault_db.exists():
            print("⚠️  Vault database not found, you need to run build_vault.py first")
            print(f"Run: python build_vault.py {self.conversation_dir} --output {self.vault_db}")
            return False

        # Step 2: Mine conversations
        if not self.run_step(
            "Mine Conversations",
            [
                'python', self.tools_dir.parent / 'mine_conversations.py',
                '--vault-db', self.vault_db,
                '--output-dir', self.output_dir / 'mining_results'
            ]
        ):
            return False

        # Step 3: Extract DNA patterns
        if not self.run_step(
            "Extract DNA Patterns",
            [
                'python', self.tools_dir / 'dna_to_prompts.py',
                '--vault-db', self.vault_db,
                '--output-dir', self.output_dir / 'prompt_dna_library',
                '--limit', '20'
            ]
        ):
            return False

        # Step 4: Extract core mechanisms
        if not self.run_step(
            "Extract Core Mechanisms",
            [
                'python', self.tools_dir / 'extract_core_mechanism.py',
                '--vault-db', self.vault_db,
                '--output-dir', self.output_dir / 'core_mechanisms',
                '--limit', '30'
            ]
        ):
            return False

        # Step 5: Find connections
        if not self.run_step(
            "Map Connection Networks",
            [
                'python', self.tools_dir / 'connection_finder.py',
                '--vault-db', self.vault_db,
                '--output', self.output_dir / 'connection_analysis.md'
            ]
        ):
            return False

        # Step 6: Analyze meta-patterns
        if not self.run_step(
            "Analyze Meta-Patterns",
            [
                'python', self.tools_dir / 'meta_pattern_analyzer.py',
                '--vault-db', self.vault_db,
                '--output', self.output_dir / 'meta_pattern_analysis.md'
            ],
            critical=False  # Non-critical
        ):
            pass  # Continue even if this fails

        # Step 7: Integrate into synthesis memory
        if not self.run_step(
            "Integrate Synthesis Memory",
            [
                'python', self.tools_dir / 'synthesis_integrator.py',
                '--synthesis-db', self.synthesis_db,
                '--mechanism-file', self.output_dir / 'core_mechanisms' / 'CORE_MECHANISM.md',
                '--dna-dir', self.output_dir / 'prompt_dna_library',
                '--connection-file', self.output_dir / 'connection_analysis.md',
                '--output', self.output_dir / 'synthesis_report.md'
            ]
        ):
            return False

        # Step 8: Generate visualizations
        if not self.run_step(
            "Generate Visualizations",
            [
                'python', self.tools_dir / 'visualize_networks.py',
                '--vault-db', self.vault_db,
                '--mechanisms', self.output_dir / 'core_mechanisms' / 'mechanisms.jsonl',
                '--connections', self.output_dir / 'connection_analysis.md',
                '--output-dir', self.output_dir / 'visualizations'
            ],
            critical=False  # Non-critical
        ):
            pass

        # Step 9 (Optional): Load into Neo4j if available
        print()
        print("="*80)
        print("OPTIONAL: Neo4j Integration")
        print("="*80)
        print()
        print("To load findings into Neo4j graph database, run:")
        print()
        print(f"  python {self.tools_dir / 'neo4j_integrator.py'} \\")
        print(f"    --vault-db {self.vault_db} \\")
        print(f"    --mechanism-file {self.output_dir / 'core_mechanisms' / 'CORE_MECHANISM.md'} \\")
        print(f"    --mechanisms-data {self.output_dir / 'core_mechanisms' / 'mechanisms.jsonl'} \\")
        print(f"    --connection-file {self.output_dir / 'connection_analysis.md'} \\")
        print(f"    --clear")
        print()

        end_time = datetime.now()
        duration = end_time - start_time

        print()
        print("="*80)
        print("PIPELINE COMPLETE")
        print("="*80)
        print()
        print(f"Duration: {duration}")
        print()
        print("📁 Results:")
        print(f"  - Mining report: {self.output_dir / 'mining_results' / 'mining_report.md'}")
        print(f"  - DNA templates: {self.output_dir / 'prompt_dna_library'}")
        print(f"  - Core mechanism: {self.output_dir / 'core_mechanisms' / 'CORE_MECHANISM.md'}")
        print(f"  - Connections: {self.output_dir / 'connection_analysis.md'}")
        print(f"  - Meta-patterns: {self.output_dir / 'meta_pattern_analysis.md'}")
        print(f"  - Synthesis report: {self.output_dir / 'synthesis_report.md'}")
        print(f"  - Visualizations: {self.output_dir / 'visualizations'}")
        print()
        print("📊 Databases:")
        print(f"  - Vault: {self.vault_db}")
        print(f"  - Synthesis: {self.synthesis_db}")
        print()
        print("✅ All archaeology steps completed successfully!")
        print()

        return True


def main():
    parser = argparse.ArgumentParser(
        description='Run full conversation archaeology pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full analysis on conversations
  python run_full_analysis.py /path/to/conversations --output /tmp/results

  # Specify custom output location
  python run_full_analysis.py ~/conversations --output ~/archaeology_results

Prerequisites:
  1. Conversation vault must be built first:
     python build_vault.py /path/to/conversations --output /tmp/vault.db

  2. Python dependencies installed:
     pip install networkx pyvis matplotlib sqlite3
        """
    )

    parser.add_argument(
        'conversation_dir',
        type=Path,
        help='Directory containing conversation files'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('/tmp/archaeology_results'),
        help='Output directory for all results (default: /tmp/archaeology_results)'
    )

    args = parser.parse_args()

    if not args.conversation_dir.exists():
        print(f"❌ Conversation directory not found: {args.conversation_dir}")
        sys.exit(1)

    pipeline = ArchaeologyPipeline(args.conversation_dir, args.output)

    success = pipeline.run()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
