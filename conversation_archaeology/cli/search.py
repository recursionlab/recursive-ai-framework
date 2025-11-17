#!/usr/bin/env python3
"""
Search CLI - Query Pattern Vault

Find conversations by:
- Domain
- Operator
- φ-depth
- Keywords (full-text)
- Novelty threshold
"""

import sys
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vault.pattern_vault import PatternVault


def print_results(results, verbose=False):
    """Pretty-print search results"""
    if not results:
        print("No results found.")
        return

    print(f"\n📊 Found {len(results)} conversations:\n")

    for i, r in enumerate(results, 1):
        novelty = r['novelty']
        phi = r['phi_depth']
        asi = '🔥' if r['proto_asi'] else '  '
        mode = r.get('thinking_mode', 'unknown')

        file_name = Path(r['file_path']).name
        if len(file_name) > 50:
            file_name = file_name[:47] + "..."

        print(f"{asi} {i:3d}. {file_name:50s}  N:{novelty:.3f}  φ{phi:2d}  [{mode}]")

        if verbose:
            print(f"       Path: {r['file_path']}")
            if r.get('bootstrap_prompt_path'):
                print(f"       Prompt: {r['bootstrap_prompt_path']}")
            print()


def search_command(vault_path: Path, args):
    """Execute search based on args"""
    vault = PatternVault(vault_path)

    if args.domain:
        print(f"🔍 Searching for domain: {args.domain}")
        results = vault.search_by_domain(args.domain, args.min_novelty, args.min_phi)
        print_results(results, args.verbose)

    elif args.operator:
        print(f"🔍 Searching for operator: {args.operator}")
        results = vault.search_by_operator(args.operator, args.min_novelty)
        print_results(results, args.verbose)

    elif args.phi_range:
        min_phi, max_phi = map(int, args.phi_range.split('-'))
        print(f"🔍 Searching for φ-depth range: φ{min_phi}-φ{max_phi}")
        results = vault.search_by_phi_depth(min_phi, max_phi)
        # Filter by novelty
        results = [r for r in results if r['novelty'] >= args.min_novelty]
        print_results(results, args.verbose)

    elif args.query:
        print(f"🔍 Full-text search: \"{args.query}\"")
        results = vault.full_text_search(args.query, args.limit)
        # Filter by novelty
        results = [r for r in results if r['novelty'] >= args.min_novelty]
        print_results(results, args.verbose)

    elif args.top:
        # Get top N by novelty
        conn = vault.db_path
        import sqlite3
        conn_obj = sqlite3.connect(conn)
        conn_obj.row_factory = sqlite3.Row
        cursor = conn_obj.cursor()

        cursor.execute('''
            SELECT * FROM conversations
            WHERE novelty >= ?
            ORDER BY novelty DESC, phi_depth DESC
            LIMIT ?
        ''', (args.min_novelty, args.top))

        results = [dict(row) for row in cursor.fetchall()]
        conn_obj.close()

        print(f"🔍 Top {args.top} by novelty")
        print_results(results, args.verbose)

    else:
        print("❌ No search criteria specified. Use --help for options.")


def stats_command(vault_path: Path):
    """Show vault statistics"""
    vault = PatternVault(vault_path)
    stats = vault.get_stats()

    print("\n📊 Vault Statistics\n")
    print(f"  Total conversations:  {stats['total_conversations']}")
    print(f"  Average novelty:      {stats['avg_novelty']:.3f}")
    print(f"  Proto-ASI emergence:  {stats['proto_asi_count']}/{stats['total_conversations']}")
    print(f"  Max φ-depth:          φ{stats['max_phi_depth']}")
    print(f"  Unique operators:     {stats['unique_operators']}")
    print(f"  Unique domains:       {stats['unique_domains']}")

    # Top operators
    print(f"\n  Top 10 operators:")
    top_ops = vault.get_top_operators(10)
    for op, count in top_ops:
        print(f"    • {op:20s} ({count} files)")


def main():
    parser = argparse.ArgumentParser(
        description="Search Pattern Vault",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search by domain
  %(prog)s --domain recursion --min-novelty 0.8

  # Search by operator
  %(prog)s --operator "Meta∘Para"

  # Search by φ-depth range
  %(prog)s --phi-range 10-20

  # Full-text search
  %(prog)s --query "semantic torsion"

  # Get top 20 by novelty
  %(prog)s --top 20

  # Show vault statistics
  %(prog)s --stats

  # Combine filters
  %(prog)s --domain torsion --min-novelty 0.9 --min-phi 10
        """
    )

    parser.add_argument(
        '--vault',
        type=Path,
        default=Path('/tmp/your_conversation_vault.db'),
        help='Path to vault database'
    )

    # Search modes
    parser.add_argument('--domain', help='Search by domain')
    parser.add_argument('--operator', help='Search by operator')
    parser.add_argument('--phi-range', help='Search by φ-depth range (e.g., 10-20)')
    parser.add_argument('--query', help='Full-text search query')
    parser.add_argument('--top', type=int, help='Get top N by novelty')
    parser.add_argument('--stats', action='store_true', help='Show vault statistics')

    # Filters
    parser.add_argument('--min-novelty', type=float, default=0.0, help='Minimum novelty')
    parser.add_argument('--min-phi', type=int, default=0, help='Minimum φ-depth')
    parser.add_argument('--limit', type=int, default=50, help='Max results for full-text search')

    # Display
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if not args.vault.exists():
        print(f"❌ Vault not found: {args.vault}")
        print(f"   Run populate_vault.py first to create the vault.")
        sys.exit(1)

    if args.stats:
        stats_command(args.vault)
    else:
        search_command(args.vault, args)


if __name__ == "__main__":
    main()
