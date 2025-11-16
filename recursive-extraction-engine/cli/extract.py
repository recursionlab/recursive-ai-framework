#!/usr/bin/env python3
"""
Main CLI for running extractions on a repository.

Usage:
  python extract.py /path/to/repo --extractors operator,equation,contradiction
  python extract.py /path/to/repo --all
  python extract.py /path/to/repo --resume
"""

import argparse
import sys
from pathlib import Path
import anthropic
import os

# Add parent dir to path so we can import from core/extractors
sys.path.insert(0, str(Path(__file__).parent.parent))

from extractors.operator_extractor import OperatorExtractor
from extractors.equation_extractor import EquationExtractor
from extractors.contradiction_extractor import ContradictionExtractor


EXTRACTORS = {
    'operator': OperatorExtractor,
    'equation': EquationExtractor,
    'contradiction': ContradictionExtractor,
    # Add more as we build them
}


def main():
    parser = argparse.ArgumentParser(
        description='Extract formal primitives from repository for Controlled Rupture framework'
    )
    parser.add_argument(
        'repo_path',
        type=Path,
        help='Path to repository to analyze'
    )
    parser.add_argument(
        '--extractors',
        type=str,
        default='all',
        help='Comma-separated list of extractors to run (operator,equation,contradiction) or "all"'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=None,
        help='Output directory (default: <repo>/extraction_outputs)'
    )
    parser.add_argument(
        '--max-workers',
        type=int,
        default=4,
        help='Number of parallel workers'
    )
    parser.add_argument(
        '--checkpoint-every',
        type=int,
        default=10,
        help='Save checkpoint every N files'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        default=None,
        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)'
    )

    args = parser.parse_args()

    # Validate repo path
    if not args.repo_path.exists():
        print(f"Error: Repository path does not exist: {args.repo_path}")
        sys.exit(1)

    # Set up output directory
    if args.output_dir is None:
        args.output_dir = args.repo_path / 'extraction_outputs'
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Get API key
    api_key = args.api_key or os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: No API key provided. Set ANTHROPIC_API_KEY env var or use --api-key")
        sys.exit(1)

    # Initialize Claude client
    claude_client = anthropic.Anthropic(api_key=api_key)

    # Determine which extractors to run
    if args.extractors == 'all':
        extractors_to_run = list(EXTRACTORS.keys())
    else:
        extractors_to_run = [e.strip() for e in args.extractors.split(',')]

    # Validate extractor names
    invalid = [e for e in extractors_to_run if e not in EXTRACTORS]
    if invalid:
        print(f"Error: Unknown extractors: {', '.join(invalid)}")
        print(f"Available: {', '.join(EXTRACTORS.keys())}")
        sys.exit(1)

    print(f"\n{'='*70}")
    print(f"RECURSIVE EXTRACTION ENGINE")
    print(f"{'='*70}")
    print(f"Repository: {args.repo_path}")
    print(f"Output: {args.output_dir}")
    print(f"Extractors: {', '.join(extractors_to_run)}")
    print(f"{'='*70}\n")

    # Run each extractor
    for extractor_name in extractors_to_run:
        extractor_class = EXTRACTORS[extractor_name]

        extractor = extractor_class(
            repo_path=args.repo_path,
            output_dir=args.output_dir,
            claude_client=claude_client,
            checkpoint_every=args.checkpoint_every,
            max_workers=args.max_workers
        )

        results = extractor.process_all()

        print(f"\n✓ {extractor_name.upper()} extraction complete: {len(results)} files processed\n")

    print(f"\n{'='*70}")
    print(f"ALL EXTRACTIONS COMPLETE")
    print(f"Results saved to: {args.output_dir}")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
