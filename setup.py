#!/usr/bin/env python3
"""
SETUP - Run This First on Fresh Clone

Generates all data files needed for the framework:
    python3 setup.py

This runs the full extraction → mapping → torsion pipeline.
Runtime: ~10-15 seconds
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name, description):
    """Run a Python script and report results"""
    print(f"\n{'='*70}")
    print(f"Running: {description}")
    print(f"{'='*70}\n")

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True
        else:
            print(f"✗ {description} failed:")
            print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print(f"✗ {description} timed out (>5 minutes)")
        return False
    except Exception as e:
        print(f"✗ {description} error: {e}")
        return False

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║  RECURSIVE AI FRAMEWORK - INITIAL SETUP                           ║
║  This will generate all data files from 524 markdown documents    ║
║  Runtime: ~10-15 seconds                                          ║
╚═══════════════════════════════════════════════════════════════════╝
    """)

    # Check if data already exists
    if Path('extraction_outputs/pattern_extraction.json').exists():
        print("⚠️  Data already exists in extraction_outputs/")
        response = input("Regenerate? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled. Run 'python3 test_everything.py' to verify.")
            return 0

    # Create output directory
    Path('extraction_outputs').mkdir(exist_ok=True)

    # Pipeline steps
    steps = [
        ('pattern_extract.py', 'Pattern Extraction (524 files → 73,949 contradictions)'),
        ('build_operator_mapping.py', 'Operator Mapping (13 symbolic → normative)'),
        ('refine_commutators.py', 'Commutator Refinement (16 evidence-based pairs)'),
        ('integrate_magnitudes.py', 'Magnitude Integration (enhanced skeleton v2.1.0)'),
        ('build_contradiction_taxonomy.py', 'Contradiction Taxonomy (6 categories)'),
        ('build_torsion_field.py', 'Torsion Field Computation (35 pairs, 17 invariants)'),
    ]

    # Run pipeline
    failed = []
    for script, description in steps:
        if not run_script(script, description):
            failed.append(description)

    # Summary
    print(f"\n{'='*70}")
    print("SETUP SUMMARY")
    print(f"{'='*70}\n")

    if not failed:
        print("✓ ALL STEPS COMPLETED SUCCESSFULLY")
        print("\nGenerated files in extraction_outputs/:")
        print("  • pattern_extraction.json (73,949 contradictions)")
        print("  • operator_mapping.json (13 mappings)")
        print("  • refined_commutators.json (16 evidence-based pairs)")
        print("  • torsion_field_analysis.json (35 torsion pairs, 17 invariants)")
        print("  • contradiction_taxonomy.json (6 categories)")
        print("\nEnhanced compiler skeleton:")
        print("  • recursive-extraction-engine/compiler/commutator_skeleton_enhanced.json")
        print("\n" + "="*70)
        print("✓ SETUP COMPLETE - System Ready")
        print("="*70)
        print("\nNext steps:")
        print("  1. Run 'python3 test_everything.py' to validate")
        print("  2. Read USAGE.md for tool documentation")
        print("  3. Run 'python3 health_check.py' for quick verification")
        return 0
    else:
        print(f"✗ {len(failed)} STEPS FAILED:")
        for step in failed:
            print(f"  • {step}")
        print("\nSetup incomplete. Check error messages above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
