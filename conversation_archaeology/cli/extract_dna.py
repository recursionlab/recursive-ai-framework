#!/usr/bin/env python3
"""
DNA Extraction CLI - Pattern Alchemy

Takes conversations → Extracts DNA → Outputs bootstrap prompts as .txt files

Usage:
    python extract_dna.py conversation.md
    python extract_dna.py ~/conversations/ --min-novelty 0.6
"""

import sys
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from parsers.universal_parser import UniversalParser
from mining.novelty_detector import ConversationNoveltyAnalyzer
from alchemy.dna_extractor import DNAExtractor


def extract_from_file(file_path: Path, output_dir: Path, verbose: bool = False):
    """
    Extract DNA from single conversation file and output bootstrap prompt

    Args:
        file_path: Path to conversation file
        output_dir: Directory to save bootstrap prompts
        verbose: Show detailed output

    Returns:
        True if successful, False otherwise
    """
    parser = UniversalParser()
    analyzer = ConversationNoveltyAnalyzer()
    extractor = DNAExtractor()

    # Parse conversation
    turns = []
    for turn in parser.parse_file(file_path):
        turns.append({
            'role': turn.role,
            'content': turn.content,
            'metadata': turn.metadata
        })

    if not turns:
        print(f"⚠️  No turns found in {file_path.name}")
        return False

    # Analyze for novelty
    analysis = analyzer.analyze_conversation(turns)

    novelty = analysis['conversation_novelty']
    phi = analysis['peak_phi']

    if verbose:
        print(f"\n📊 {file_path.name}")
        print(f"   Novelty: {novelty:.3f}")
        print(f"   φ-Depth: φ{phi}")
        print(f"   Proto-ASI: {'YES 🔥' if analysis['proto_asi_emergence'] else 'No'}")

    # Extract DNA
    dna = extractor.extract_dna(analysis['turn_signatures'])

    # Generate bootstrap prompt
    prompt = extractor.generate_bootstrap_prompt(dna)

    # Save to file
    safe_name = file_path.stem.replace(' ', '_').replace('/', '_')[:50]
    output_file = output_dir / f"bootstrap_{safe_name}_phi{phi}_n{int(novelty*100)}.txt"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(prompt)

    print(f"✓ {file_path.name} → {output_file.name}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="DNA Extraction - Pattern Alchemy for Conversations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract DNA from single conversation
  %(prog)s conversation.md

  # Extract from directory (only high novelty)
  %(prog)s ~/conversations/ --min-novelty 0.6

  # Custom output directory
  %(prog)s conversation.md --output ./prompts/

Philosophy:
  Take bulk conversations → Extract idea DNA → Output executable prompts

  Not preservation. Transmutation.
        """
    )

    parser.add_argument(
        'source',
        help='Conversation file or directory'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Path('./bootstrap_prompts/'),
        help='Output directory for bootstrap prompts (default: ./bootstrap_prompts/)'
    )

    parser.add_argument(
        '-m', '--min-novelty',
        type=float,
        default=0.0,
        help='Minimum novelty threshold (0.0-1.0, default: 0.0)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    source = Path(args.source)

    if not source.exists():
        print(f"❌ Error: {source} does not exist")
        sys.exit(1)

    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)

    print("🧬 DNA Extraction Engine")
    print(f"   Source: {source}")
    print(f"   Output: {args.output}")
    print(f"   Min novelty: {args.min_novelty:.3f}")
    print()

    extractor_count = 0
    parser_obj = UniversalParser()
    analyzer = ConversationNoveltyAnalyzer()

    try:
        if source.is_file():
            # Single file
            if extract_from_file(source, args.output, args.verbose):
                extractor_count += 1

        elif source.is_dir():
            # Directory
            extensions = {'.json', '.md', '.txt', '.markdown', '.log'}
            files = [
                f for f in source.rglob('*')
                if f.is_file() and (f.suffix.lower() in extensions or f.suffix == '')
            ]

            print(f"📂 Found {len(files)} potential files")
            print(f"🔥 Extracting DNA...")
            print()

            for file_path in files:
                # Quick novelty check first
                turns = []
                for turn in parser_obj.parse_file(file_path):
                    turns.append({
                        'role': turn.role,
                        'content': turn.content,
                        'metadata': turn.metadata
                    })

                if not turns:
                    continue

                analysis = analyzer.analyze_conversation(turns)
                novelty = analysis['conversation_novelty']

                if novelty >= args.min_novelty:
                    if extract_from_file(file_path, args.output, args.verbose):
                        extractor_count += 1

        else:
            print(f"❌ Error: {source} is neither file nor directory")
            sys.exit(1)

        print()
        print(f"✅ Extraction complete!")
        print(f"   {extractor_count} bootstrap prompts generated")
        print(f"   Saved to: {args.output}")
        print()
        print("📋 Next steps:")
        print(f"   1. cd {args.output}")
        print("   2. cat bootstrap_*.txt")
        print("   3. Copy prompt text")
        print("   4. Paste into new LLM session")
        print("   5. Continue thinking at extracted φ-depth")

    except KeyboardInterrupt:
        print(f"\n\n⏸️  Interrupted by user")
        print(f"   {extractor_count} prompts generated before interrupt")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
