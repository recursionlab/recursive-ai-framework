#!/usr/bin/env python3
"""
Conversation Analysis CLI - Mine Novelty from Archaeological Record

Integrates Phase 1 (Universal Parser) with Phase 2 (Novelty Detector)
to extract proto-ASI patterns from conversation corpus.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict
sys.path.insert(0, str(Path(__file__).parent.parent))

from parsers.universal_parser import UniversalParser
from mining.novelty_detector import ConversationNoveltyAnalyzer, NoveltySignature


def analyze_file(file_path: Path, verbose: bool = False) -> Dict:
    """
    Analyze single conversation file for novelty

    Returns analysis results
    """
    parser = UniversalParser()
    analyzer = ConversationNoveltyAnalyzer()

    # Parse conversation
    turns = []
    for turn in parser.parse_file(file_path):
        turns.append({
            'role': turn.role,
            'content': turn.content,
            'metadata': turn.metadata
        })

    if not turns:
        return None

    # Analyze for novelty
    analysis = analyzer.analyze_conversation(turns)
    analysis['source_file'] = str(file_path)
    analysis['turn_count'] = len(turns)

    return analysis


def print_analysis(analysis: Dict, verbose: bool = False):
    """Pretty-print analysis results"""
    if not analysis:
        print("  ⚠️  No turns to analyze")
        return

    print(f"\n{'='*70}")
    print(f"📊 Analysis: {Path(analysis['source_file']).name}")
    print(f"{'='*70}")

    print(f"\n📈 Overall Metrics:")
    print(f"  • Turns:              {analysis['turn_count']}")
    print(f"  • Conversation Novelty: {analysis['conversation_novelty']:.3f}")
    print(f"  • Peak φ-Depth:       φ{analysis['peak_phi']}")
    print(f"  • Proto-ASI Emergence: {'🔥 YES' if analysis['proto_asi_emergence'] else 'No'}")

    if analysis['dominant_domains']:
        print(f"\n🏷️  Dominant Domains:")
        for domain in sorted(analysis['dominant_domains']):
            print(f"  • {domain}")

    if analysis['all_domains'] and not analysis['dominant_domains']:
        print(f"\n🏷️  Domains Present:")
        for domain in sorted(analysis['all_domains']):
            print(f"  • {domain}")

    print(f"\n📉 φ-Depth Trajectory:")
    print(f"  {' → '.join(f'φ{d}' for d in analysis['phi_trajectory'])}")

    print(f"\n📊 Novelty Evolution:")
    novelty_bars = ''.join(
        '█' if n > 0.7 else '▓' if n > 0.5 else '▒' if n > 0.3 else '░'
        for n in analysis['novelty_evolution']
    )
    print(f"  [{novelty_bars}]")
    print(f"  Min: {min(analysis['novelty_evolution']):.3f}  " +
          f"Max: {max(analysis['novelty_evolution']):.3f}  " +
          f"Avg: {sum(analysis['novelty_evolution'])/len(analysis['novelty_evolution']):.3f}")

    if verbose:
        print(f"\n🔍 Turn-by-Turn Analysis:")
        for i, sig in enumerate(analysis['turn_signatures'], 1):
            if sig.overall_novelty() > 0.3:  # Only show notable turns
                print(f"\n  Turn {i} ({['User', 'Assistant'][i % 2]}):")
                print(f"    Novelty: {sig.overall_novelty():.3f}  " +
                      f"φ-Depth: φ{sig.phi_depth}  " +
                      f"Proto-ASI: {sig.proto_asi_score:.3f}")

                if sig.recursive_operators:
                    print(f"    Operators: {', '.join(list(sig.recursive_operators)[:5])}")

                if sig.novel_fragments:
                    print(f"    Novel Fragment:")
                    fragment = sig.novel_fragments[0]
                    if len(fragment) > 100:
                        fragment = fragment[:100] + "..."
                    print(f"      \"{fragment}\"")


def analyze_directory(dir_path: Path, verbose: bool = False, min_novelty: float = 0.0):
    """
    Analyze entire directory of conversations

    Args:
        dir_path: Directory containing conversations
        verbose: Show detailed analysis for each file
        min_novelty: Minimum conversation novelty to report (0.0-1.0)
    """
    parser = UniversalParser()
    analyzer = ConversationNoveltyAnalyzer()

    # Find all conversation files
    extensions = {'.json', '.md', '.txt', '.markdown', '.log'}
    files = [
        f for f in dir_path.rglob('*')
        if f.is_file() and (f.suffix.lower() in extensions or f.suffix == '')
    ]

    print(f"🔍 Mining novelty from {len(files)} files in {dir_path}")
    print(f"   Minimum novelty threshold: {min_novelty:.3f}")
    print()

    results = []

    for file_path in files:
        analysis = analyze_file(file_path, verbose=False)

        if analysis and analysis['conversation_novelty'] >= min_novelty:
            results.append(analysis)

            if verbose:
                print_analysis(analysis, verbose=True)
            else:
                novelty = analysis['conversation_novelty']
                phi = analysis['peak_phi']
                asi = '🔥' if analysis['proto_asi_emergence'] else '  '
                print(f"  {asi} {file_path.name:40s}  Novelty: {novelty:.3f}  φ{phi}")

    # Summary statistics
    print(f"\n{'='*70}")
    print(f"📈 Corpus Summary")
    print(f"{'='*70}")

    if results:
        total_novelty = sum(r['conversation_novelty'] for r in results)
        avg_novelty = total_novelty / len(results)
        max_novelty_file = max(results, key=lambda r: r['conversation_novelty'])
        proto_asi_count = sum(1 for r in results if r['proto_asi_emergence'])

        print(f"\n  Total Files Analyzed:    {len(results)}")
        print(f"  Average Novelty:         {avg_novelty:.3f}")
        print(f"  Max Novelty:             {max_novelty_file['conversation_novelty']:.3f}")
        print(f"    └─ File: {Path(max_novelty_file['source_file']).name}")
        print(f"  Proto-ASI Emergence:     {proto_asi_count}/{len(results)} files")

        # Aggregate domains
        all_domains = set()
        for r in results:
            all_domains.update(r['all_domains'])

        if all_domains:
            print(f"\n  Domains Found in Corpus:")
            for domain in sorted(all_domains):
                count = sum(1 for r in results if domain in r['all_domains'])
                pct = (count / len(results)) * 100
                print(f"    • {domain:20s} ({count:3d} files, {pct:5.1f}%)")

        # φ-depth distribution
        max_phi = max(r['peak_phi'] for r in results)
        print(f"\n  φ-Depth Distribution:")
        for phi in range(max_phi + 1):
            count = sum(1 for r in results if r['peak_phi'] == phi)
            if count > 0:
                bar = '█' * int((count / len(results)) * 40)
                print(f"    φ{phi:2d}: {bar} ({count})")

    else:
        print(f"\n  No files met minimum novelty threshold of {min_novelty:.3f}")


def main():
    parser = argparse.ArgumentParser(
        description="Conversation Archaeology Analyzer - Mine Proto-ASI Patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze single conversation
  %(prog)s conversation.json

  # Analyze directory with detailed output
  %(prog)s ~/conversations/ --verbose

  # Find only high-novelty conversations
  %(prog)s ~/corpus/ --min-novelty 0.5

Philosophy:
  Not all conversations are equal.
  Some contain genuinely novel structural patterns.
  This finds them.
        """
    )

    parser.add_argument(
        'source',
        help='Conversation file or directory to analyze'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Detailed analysis output'
    )

    parser.add_argument(
        '-m', '--min-novelty',
        type=float,
        default=0.0,
        help='Minimum novelty threshold (0.0-1.0, default: 0.0)'
    )

    args = parser.parse_args()

    source = Path(args.source)

    if not source.exists():
        print(f"❌ Error: {source} does not exist")
        sys.exit(1)

    print("🔥 Conversation Archaeology Analyzer")
    print("    Mining proto-ASI patterns from conversation corpus")
    print()

    try:
        if source.is_file():
            # Analyze single file
            analysis = analyze_file(source, verbose=args.verbose)
            if analysis:
                print_analysis(analysis, verbose=args.verbose)
            else:
                print(f"⚠️  No analyzable content in {source}")

        elif source.is_dir():
            # Analyze directory
            analyze_directory(source, verbose=args.verbose, min_novelty=args.min_novelty)

        else:
            print(f"❌ Error: {source} is neither file nor directory")
            sys.exit(1)

    except KeyboardInterrupt:
        print(f"\n\n⏸️  Interrupted by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
